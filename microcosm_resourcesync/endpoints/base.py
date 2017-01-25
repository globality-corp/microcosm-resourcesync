"""
Endpoint interface

"""
from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class Endpoint(object):
    """
    An endpoint is able to read and write resources.

    """
    @abstractmethod
    def read(self, resource_cls):
        """
        Generate resource lists of the given class.

        """
        pass

    @abstractmethod
    def write(self, resources, formatter, remove_first):
        """
        Write resources using the given formatter.

        """
        pass

    def validate_for_read(self, resource_cls):
        """
        Validate that reading is possible.

        """
        pass

    def validate_for_write(self, formatter, remove_first):
        """
        Validate that writing is possible.

        """
        pass
