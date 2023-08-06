from .identifier import *
from .utils import get_tmp_path


class InputVisitor:

    def __init__(self, f):
        self.f = f
        self.cases = {}

    # Create hash map for each dtype
    def case(self, _format):

        def call(fun):
            self.cases[_format] = fun

        return call

    def __call__(self, arg1, arg2):
        fun = self.cases[arg2]
        return fun(arg1)


class ArchVisitor:

    def __init__(self, f):
        self.f = f
        self.cases = {}

    def case(self, _format):

        def call(fun):
            self.cases[_format] = fun

        return call

    def __call__(self, arg1, arg2):
        fun = self.cases[arg2]
        return fun(arg1)


@InputVisitor
def _get_input(x, format):
    pass


@ArchVisitor
def _get_arch(x, format):
    pass


@_get_arch.case(H5)
def h5_arch(path):
    """
    Draw dot graph of model architecture
    """
    from keras.utils.vis_utils import plot_model
    from tensorflow import keras
    model = keras.models.load_model(path)
    output_path = get_tmp_path()+'.png'
    plot_model(model, to_file=output_path, show_shapes=True,
               show_layer_names=True)
    return output_path


@_get_input.case(H5)
def h5_file(path):
    from tensorflow import keras
    model = keras.models.load_model(path)
    return [x.name for x in model.inputs]


@_get_input.case(ONNX)
def onnx_file(path):
    # https://github.com/onnx/onnx/issues/2657
    import onnx
    model = onnx.load(path)

    input_all = [node.name for node in model.graph.input]
    input_initializer = [node.name for node in model.graph.initializer]
    net_feed_input = list(set(input_all) - set(input_initializer))

    return net_feed_input


def get_input(model):
    fi = FormatIdentifier()
    model_type = fi.identify(model)
    return _get_input(model, model_type)


def get_arch(model):
    fi = FormatIdentifier()
    model_type = fi.identify(model)
    return _get_arch(model, model_type)
