#! /usr/bin/python
# -*- coding: utf-8 -*-

from .common import str2act, str2init
from .common import _save_weights, _load_weights
from mindspore.nn import Cell
import tensorlayer as tl
from collections import OrderedDict

from mindspore import log as logger
import inspect
from mindspore import context
import numpy
import mindspore as ms
from mindspore.common.api import _pynative_exec
from mindspore.common.parameter import Parameter

__all__ = ['Module', 'SequentialLayer']

_global_layer_name_dict = {}  # TODO: better implementation?


class Module(Cell):

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

        # data_format
        self.data_format = "NCHW"

    def forward(self, *inputs, **kwargs):
        raise Exception("The forward method must be implemented by inherited class")

    def construct(self, *inputs, **kwargs):
        return self.forward(*inputs, **kwargs)

    def build(self, inputs_shape):
        raise Exception("The build(self, inputs_shape) method must be implemented by inherited class")

    def _get_weights(
        self, var_name, shape, init=tl.initializers.random_normal(), trainable=True, transposed=False, order=False
    ):
        """ Get trainable variables. """
        var_name = self.name + "/" + var_name
        # TODO 2D mindspore weights shape : [out_channel, in_channel, kernel_h, kernel_w]
        # TODO 2D mindspore transposed shape [in_channel, out_channel, kernel_h, kernel_w]
        if order:
            initial_value = init(shape=shape)
            return tl.Variable(initial_value=initial_value, name=var_name, trainable=trainable)

        if len(shape) == 3:
            shape = shape[::-1]
        if len(shape) == 4:
            if not transposed and self.data_format == 'NHWC':
                shape = (shape[3], shape[0], shape[1], shape[2])
            else:
                shape = (shape[3], shape[2], shape[0], shape[1])
        if len(shape) == 5:
            shape = (shape[4], shape[3], shape[0], shape[1], shape[2])

        initial_value = init(shape=shape)
        var = tl.Variable(initial_value=initial_value, name=var_name, trainable=trainable)
        self.trainable = trainable
        return var

    def save_weights(self, file_path, format=None):
        """Input file_path, save model weights into a file of given format."""
        _save_weights(self, file_path, format)

    def load_weights(self, file_path, format=None, in_order=True, skip=False):
        """Load model weights from a given file, which should be previously saved by self.save_weights()."""
        _load_weights(self, file_path, format, in_order, skip)

    @staticmethod
    def _compute_shape(tensors):
        if isinstance(tensors, list):
            shape_mem = [tl.get_tensor_shape(t) for t in tensors]
        else:
            shape_mem = tl.get_tensor_shape(tensors)
        return shape_mem

    def __call__(self, *inputs, **kwargs):
        if self.__class__.construct is Cell.construct:
            logger.warning(
                f"The '{self.__class__}' does not override the method 'construct', "
                f"will call the super class(Cell) 'construct'."
            )
        if kwargs:
            bound_args = inspect.signature(self.construct).bind(*inputs, **kwargs)
            inputs = bound_args.args
            kwargs = bound_args.kwargs

        if context.get_context("mode") == context.GRAPH_MODE:
            raise NotImplemented("GRAPH MODE is not supported, please select PYNATIVE MODE.")

        # if context.get_context("mode") == context.GRAPH_MODE:
        #     if kwargs:
        #         raise ValueError("For 'graph' mode, the outermost network does not support passing "
        #                          "variable key-value pair parameters.")
        #     if self.enable_hook:
        #         raise ValueError("The graph mode does not support hook function.")
        #     out = self.compile_and_run(*inputs)
        #     return out

        self.do_parameter_broadcast()
        for item in inputs:
            if isinstance(item, numpy.ndarray):
                raise TypeError("cell inputs should not be numpy array.")
        origin_grad = []
        if self.requires_grad is True:
            _pynative_exec.set_grad_flag(True)
            _pynative_exec.new_graph(self, *inputs, **kwargs)
            for cell in self.cells():
                origin_grad.append(cell.requires_grad)
                cell.set_grad(True)
        else:
            _pynative_exec.set_grad_flag(False)
        cast_inputs = list()
        if hasattr(self, "_mindspore_flags"):
            if self._mindspore_flags.get('fp16'):
                cast_inputs = self._cast_mixed_precision_inputs(inputs, ms.float16)
            if self._mindspore_flags.get('fp32'):
                cast_inputs = self._cast_mixed_precision_inputs(inputs, ms.float32)
        if not cast_inputs:
            cast_inputs = inputs
        output = self.run_construct(cast_inputs, kwargs)
        if isinstance(output, Parameter):
            output = output.data
        if self.requires_grad is True:
            _pynative_exec.end_graph(self, output, *inputs, **kwargs)
            for i, cell in enumerate(self.cells()):
                cell.set_grad(origin_grad[i])
        return output

    def _add_node(self, input_tensors, output_tensors):
        """Add a LayerNode for this layer given input_tensors, output_tensors.

        WARINING: This function should not be called from outside, it should only be called
        in layer.__call__ when building static model.

        Parameters
        ----------
        input_tensors : Tensor or a list of tensors
            Input tensors to this layer.
        output_tensors : Tensor or a list of tensors
            Output tensors to this layer.

        """
        raise NotImplementedError

    def set_train(self):
        """
        Sets the cell to training mode.

        The cell itself and all children cells will be set to training mode.

        Args:
            mode (bool): Specifies whether the model is training. Default: True.
        """
        self._phase = 'train'
        self.add_flags_recursive(training=True)
        return self

    def set_eval(self):
        """Set this network in evaluation mode. After calling this method,
        all layers in network are in evaluation mode, in particular, BatchNorm, Dropout, etc.

        Examples
        --------
        >>> import tensorlayer as tl
        >>> net = tl.models.vgg16()
        >>> net.eval()
        # do evaluation

        """
        self._phase = 'predict'
        self.add_flags_recursive(training=False)
        return self

    def test(self):
        """Set this network in evaluation mode."""
        self.eval()

    def infer(self):
        """Set this network in evaluation mode."""
        self.eval()

    @property
    def trainable_weights(self):
        """
        Returns all trainable weights.

        Returns a list of all trainable parmeters.

        Args:
            recurse (bool): Whether contains the trainable weights of sublayers. Default: True.

        Returns:
            List, the list of trainable weights.
        """
        self._trainable_weights = list(filter(lambda x: x.requires_grad, self.get_parameters(expand=True)))
        return self._trainable_weights

    @property
    def nontrainable_weights(self):
        """
        Returns all untrainable weights.

        Returns a list of all untrainable weights.

        Args:
            recurse (bool): Whether contains the untrainable weights of sublayers. Default: True.

        Returns:
            List, the list of untrainable weights.
        """
        return list(filter(lambda x: not x.requires_grad, self.get_parameters(expand=True)))

    @property
    def all_weights(self):
        return list(filter(lambda x: x.requires_grad, self.get_parameters(expand=True))) \
               + list(filter(lambda x: not x.requires_grad, self.get_parameters(expand=True)))

    def str_to_init(self, initializer):
        return str2init(initializer)


class SequentialLayer(Module):
    """
    The class :class:`SequentialLayer` is a linear stack of layers.
    The :class:`SequentialLayer` can be created by passing a list of layer instances.
    The given layer instances will be automatically connected one by one.
    Parameters
    ----------
    layers: list of Layer
        A list of layers.
    name : str or None
        A unique layer name. If None, a unique name will be automatically assigned.
    Methods
    ---------
    __init__()
        Initializing the LayerList.
    weights()
        A collection of weights of all the layer instances.
    build()
        Build the LayerList. The layer instances will be connected automatically one by one.
    forward()
        Forward the computation. The computation will go through all layer instances.

    Examples
    ---------
    >>> conv = tl.layers.Conv2d(3, 2, 3, pad_mode='valid')
    >>> bn = tl.layers.BatchNorm2d(2)
    >>> seq = tl.layers.SequentialLayer([conv, bn])
    >>> x = tl.layers.Input((1, 3, 4, 4))
    >>> seq(x)

    """

    def __init__(self, *args):
        super(SequentialLayer, self).__init__()
        # self._built = True
        if len(args) == 1:
            layers = args[0]
            if isinstance(layers, list):
                for index, layer in enumerate(layers):
                    self.insert_child_to_layer(str(index), layer)
            elif isinstance(layers, OrderedDict):
                for name, layer in layers.items():
                    self.insert_child_to_layer(name, layer)
            else:
                raise TypeError('Layers must be list or orderedDict')
        else:
            for index, layer in enumerate(args):
                self.insert_child_to_layer(str(index), layer)
        self.layer_list = list(self._layers.values())

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__class__(OrderedDict(list(self._layers.items())[index]))
        index = self._valid_index(len(self), index)
        return list(self._layers.values())[index]

    def __setitem__(self, index, layer):
        if self._valid_module(layer):
            index = self._valid_index(len(self), index)
            key = list(self._layers.keys())[index]
            self._layers[key] = layer
            self.layer_list = list(self._layers.values())

    def __delitem__(self, index):
        if isinstance(index, int):
            index = self._valid_index(len(self), index)
            key = list(self._layers.keys())[index]
            del self._layers[key]
        elif isinstance(index, slice):
            keys = list(self._layers.keys())[index]
            for key in keys:
                del self._layers[key]
        else:
            raise TypeError('Index {} is not int type or slice type'.format(index))
        self.layer_list = list(self._layers.values())

    def __len__(self):
        return len(self._layers)

    def set_grad(self, flag=True):
        self.requires_grad = flag
        for layer in self._layers.values():
            layer.set_grad(flag)

    def append(self, layer):
        if self._valid_module(layer):
            self._layers[str(len(self))] = layer
        self.layer_list = list(self._layers.values())
        return self

    def build(self, inputs_shape):
        pass

    def forward(self, input_data):
        for layer in self.layer_list:
            input_data = layer(input_data)
        return input_data

    def _valid_index(self, layer_num, index):
        if not isinstance(index, int):
            raise TypeError("Index {} is not int type")
        if not -layer_num <= index < layer_num:
            raise IndexError(
                "Index should be a number in range [{}, {}), but got {}".format(-layer_num, layer_num, index)
            )
        return index % layer_num

    def _valid_module(self, layer):
        if issubclass(layer.__class__, Module):
            return True
        raise TypeError('Module {} is not subclass of Module'.format(layer))
