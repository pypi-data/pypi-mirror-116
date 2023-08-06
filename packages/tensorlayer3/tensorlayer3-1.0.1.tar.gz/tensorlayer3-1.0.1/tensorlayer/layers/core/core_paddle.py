#! /usr/bin/python
# -*- coding: utf-8 -*-

import copy, six
from .common import str2act, str2init
from .common import _save_weights, _load_weights
from paddle.fluid import framework
from paddle.fluid.dygraph import Layer
from paddle.fluid.framework import in_dygraph_mode
from paddle.fluid.dygraph.base import program_desc_tracing_guard, param_guard
from paddle.fluid.dygraph import parallel_helper
import paddle as pd

_global_layer_name_dict = {}

__all__ = ['Module']


class Module(Layer):

    def __init__(self, name=None, act=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        global _global_layer_name_dict
        if name is None:
            prefix = self.__class__.__name__.lower()

            if _global_layer_name_dict.get(prefix) is not None:
                _global_layer_name_dict[prefix] += 1
                name = prefix + '_' + str(_global_layer_name_dict[prefix])
            else:
                _global_layer_name_dict[prefix] = 0
                name = prefix
            while True:
                if _global_layer_name_dict.get(name) is None:
                    break
                _global_layer_name_dict[prefix] += 1
                name = prefix + '_' + str(_global_layer_name_dict[prefix])
        else:
            if _global_layer_name_dict.get(name) is not None:
                pass
            else:
                _global_layer_name_dict[name] = 0

        self.name = name

        if isinstance(act, str):
            str_act = str2act(act)

        if act:
            if isinstance(act, str) and (len(act) > 5 and act[0:5] == "lrelu" or
                                         len(act) > 10 and act[0:10] == "leaky_relu"):
                self.act = str_act
            elif isinstance(act, str):
                self.act = str_act()
            else:
                self.act = act()
        else:
            self.act = act

        # Layer building state
        self._built = False

        # paddl_built
        self._paddle_built = False

        # Layer nodes state
        self._nodes = []
        self._nodes_fixed = False

        # Layer weight state
        self._all_weights = []
        self._trainable_weights = []
        self._nontrainable_weights = []

        # Layer training state
        self.is_train = True

        # layer forward  state
        self._forward_state = False

    def set_train(self):
        """
        Sets this Layer and all its sublayers to training mode.
        This only effects certain modules like `Dropout` and `BatchNorm`.

        Returns:
            None

        Example::
            .. code-block:: python

                import paddle

                class MyLayer(paddle.nn.Layer):
                    def __init__(self):
                        super(MyLayer, self).__init__()
                        self._linear = paddle.nn.Linear(1, 1)
                        self._dropout = paddle.nn.Dropout(p=0.5)

                    def forward(self, input):
                        temp = self._linear(input)
                        temp = self._dropout(temp)
                        return temp

                x = paddle.randn([10, 1], 'float32')
                mylayer = MyLayer()
                mylayer.eval()  # set mylayer._dropout to eval mode
                out = mylayer(x)
                mylayer.train()  # set mylayer._dropout to train mode
                out = mylayer(x)

        """
        # global setting in dygraph
        # NOTE(chenweihang): nn.Layer also can be used in static mode,
        # but _dygraph_tracer() can not be called in static mode
        if in_dygraph_mode():
            framework._dygraph_tracer().train_mode()
        # Layer-level setting
        self.is_train = True
        for layer in self.sublayers():
            layer.is_train = True

    def set_eval(self):
        """
        Sets this Layer and all its sublayers to evaluation mode.
        This only effects certain modules like `Dropout` and `BatchNorm`.

        Returns:
            None

        Example::
            .. code-block:: python

                import paddle

                class MyLayer(paddle.nn.Layer):
                    def __init__(self):
                        super(MyLayer, self).__init__()
                        self._linear = paddle.nn.Linear(1, 1)
                        self._dropout = paddle.nn.Dropout(p=0.5)

                    def forward(self, input):
                        temp = self._linear(input)
                        temp = self._dropout(temp)
                        return temp

                x = paddle.randn([10, 1], 'float32')
                mylayer = MyLayer()
                mylayer.eval()  # set mylayer._dropout to eval mode
                out = mylayer(x)
                print(out)

        """
        # global setting in dygraph
        # NOTE(chenweihang): nn.Layer also can be used in static mode,
        # but _dygraph_tracer() can not be called in static mode
        if in_dygraph_mode():
            framework._dygraph_tracer().eval_mode()
        # Layer-level setting
        self.is_train = False
        for layer in self.sublayers():
            layer.is_train = False

    def build(self, inputs_shape):
        raise Exception("The build(self, inputs_shape) method must be implemented by inherited class")

    def forward(self, *inputs, **kwargs):
        raise Exception("The forward method must be implemented by inherited class")

    def __call__(self, *inputs, **kwargs):
        with param_guard(self._parameters), param_guard(self._buffers):
            for forward_pre_hook in self._forward_pre_hooks.values():
                hook_result = forward_pre_hook(self, inputs)
                if hook_result is not None:
                    if not isinstance(hook_result, tuple):
                        hook_result = (hook_result, )
                    inputs = hook_result

            if not self._paddle_built:
                with program_desc_tracing_guard(False):
                    self._build_once(*inputs, **kwargs)
                    if parallel_helper._is_data_parallel_mode():
                        parallel_helper._broadcast_parameters(self._parameters.values())
                self._paddle_built = True

            outputs = self.forward(*inputs, **kwargs)

            for forward_post_hook in self._forward_post_hooks.values():
                hook_result = forward_post_hook(self, inputs, outputs)
                if hook_result is not None:
                    outputs = hook_result

            return outputs

    def _get_weights(self, var_name, shape, init=None, trainable=True, transposed=None, order=False):
        # TODO 2D mindspore weights shape : [out_channel, in_channel, kernel_h, kernel_w]
        # TODO 2D mindspore transposed shape [in_channel, out_channel, kernel_h, kernel_w]
        var_name = self.name + "/" + var_name

        if order:
            w_tmp = self.create_parameter(shape=shape, attr=init, var_name=var_name, trainable=trainable)
            return w_tmp

        if len(shape) == 3:
            shape = shape[::-1]
        if len(shape) == 4:
            if transposed:
                shape = (shape[3], shape[0], shape[1], shape[2])
            else:
                shape = (shape[3], shape[2], shape[0], shape[1])
        if len(shape) == 5:
            shape = (shape[4], shape[3], shape[0], shape[1], shape[2])

        w_tmp = self.create_parameter(shape=shape, attr=init, var_name=var_name, trainable=trainable)

        return w_tmp

    def create_parameter(
        self, shape, attr=None, dtype=None, is_bias=False, default_initializer=None, trainable=True, var_name=None
    ):
        """Create parameters for this layer."""
        init_attr = pd.ParamAttr(name=var_name, initializer=attr, trainable=trainable, do_model_average=True)
        temp_attr = copy.deepcopy(init_attr)
        if isinstance(temp_attr, six.string_types) and temp_attr == "":
            temp_attr = None
        return self._helper.create_parameter(temp_attr, shape, dtype, is_bias, default_initializer)

    @property
    def all_weights(self):
        ret = [param for _, param in self.named_parameters(include_sublayers=True)]
        return ret

    @property
    def trainable_weights(self):
        return self.parameters()

    def init_build(self, *inputs, **kwargs):
        """
        (1) This method must be called when the Layer has no input in_channels.
        (2) Automatic shape inference when the user does not enter inchannels.
        """

        self.forward(*inputs, **kwargs)

    def save_weights(self, file_path, format=None):
        _save_weights(net=self, file_path=file_path, format=format)

    def load_weights(self, file_path, format=None, in_order=True, skip=False):
        """Load model weights from a given file, which should be previously saved by self.save_weights()."""
        _load_weights(net=self, file_path=file_path, format=format, in_order=in_order, skip=skip)

    def str_to_init(self, initializer):
        return str2init(initializer)
