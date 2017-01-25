"""
Resource interface.

"""
from abc import ABCMeta, abstractproperty
from six import add_metaclass


@add_metaclass(ABCMeta)
class Resource(dict):
    """
    A resource wraps a dictionary and defines a `uri`, `id`, and `type`.

    """
    @property
    def id(self):
        """
        A resource dictionary is assumed to have an "id" attribute.

        """
        return self["id"]

    @abstractproperty
    def type(self):
        pass

    @abstractproperty
    def uri(self):
        pass
