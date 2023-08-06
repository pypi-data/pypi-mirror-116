from abc import ABC, abstractmethod
from typing import Union
import os
from .utils import get_tmp_path
import inspect
import sys
import inspect


def _check_object_type(expect_type_str, object):
    type_str = ""
    try:
        type_str += str(inspect.getmro((model)))
    except:
        type_str += ""
    type_str += "|"
    type_str += str(type(object))
    return expect_type_str in type_str


class ModelSerializer(ABC):
    """Abstract class to serialize a model

    The class uses Command Chain design pattern and work with
    `SerializerSelector` to select corresponding Serializer

    """
    format: str = None

    @classmethod
    @abstractmethod
    def is_me(cls, model: object):
        """Identify if this class can handle the given model

        :param model: A model object
        :type model: object

        :return: If the object should be handled by this class.
        :rtype: int
        """
        pass

    @abstractmethod
    def serialize(self, model: object, path: str = None):
        """Serialize the given model

        :param model: A model object
        :type object
        :param path: output path, if not provied, a temp path will
                      be used.
        :type str

        :return: The path to serialized model.
        :rtype: str
        """
        pass


class TFKerasSerializer(ModelSerializer):
    ''' Tensorflow2 Keras Serializer
    '''

    format = 'H5'

    @classmethod
    def is_me(cls, model):
        if _check_object_type('tensorflow.python.keras', model):
            return True
        else:
            return False

    def serialize(self, model, path=None):
        if not path:
            path = get_tmp_path() + '.h5'

        model.save(path)

        return path


class KerasSerializer(ModelSerializer):
    '''
    Keras 2.5.0 Serializer
    '''

    format = 'H5'

    @classmethod
    def is_me(cls, model):
        if _check_object_type('keras.', model):
            return True
        else:
            return False

    def serialize(self, model, path=None):
        if not path:
            path = get_tmp_path() + '.h5'

        model.save(path)

        return path


class PytorchSerializer(ModelSerializer):
    """Seriealize a torch.nn.moduel into a onnx file"""
    
    format = 'TorchONNX'

    @classmethod
    def is_me(cls, model):
        if _check_object_type('torch.nn.module', model):
            return True
        else:
            return False

    def serialize(self, model, path=None, shape=None):
        if not path:
            path = get_tmp_path() + '.onnx'
        if not shape:
            raise Exception(f"Parameter `shape` is required using {str(self.__class__)}")

        try:
            if not all(isinstance(x, int) for x in shape):
                raise Exception(f"Parameter `shape` must be List[int]")
        except:
            raise Exception(f"Parameter `shape` must be List[int]")

        dummy_input = torch.rand(*shape)
        torch.onnx.export(model, (dummy_input, ),
                          path)

        return path


class TF1Serializer(ModelSerializer):
    """Not NotImplemented Yet"""
    pass


class TF2Serializer(ModelSerializer):
    """Not NotImplemented Yet"""
    pass


class SerializerSelector(ABC):
    """Select a serializer according to format
    """
    @property
    @abstractmethod
    def serializers(self):
        raise NotImplementedError

    def __init__(self):
        pass

    @classmethod
    def register(cls, serializer):
        """Register a supported serializer

        :param serializer: A serializer class
        :type serializer: Could be any type of serializer
        """
        cls.serializers.add(serializer)

    @classmethod
    def select(cls, format: format):
        """Select a serializer according to input format

        :return: A serializer
        :rtype: Could be any type of serializer

        """
        for c in cls.serializers:
            if c.is_me(format):
                return c

        raise Exception(f'Unable to serialize obj type: {type(format)}')


class ModelSerializerSelector(SerializerSelector):
    category = "model"
    serializers = set()

    def __init__(self):
        super().__init__()


# Auto register
for name, obj in inspect.getmembers(sys.modules[__name__]):
    # Model
    if inspect.isclass(obj) and issubclass(
            obj, ModelSerializer) and obj.__name__ != "ModelSerializer":
        ModelSerializerSelector.register(obj)
