"""
Formatter interface

"""
from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class Formatter(object):
    """
    A format encodes a resource to/from a dictionary.

    """
    @abstractmethod
    def load(self, data):
        """
        Load input data into a dictionary.

        """
        pass

    @abstractmethod
    def dump(self, dct):
        """
        Dump a resource dictionary into encoded data.

        """
        pass
