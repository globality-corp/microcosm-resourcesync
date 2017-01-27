"""
Schema interface.

"""
from abc import ABCMeta, abstractmethod, abstractproperty
from six import add_metaclass


@add_metaclass(ABCMeta)
class Schema(dict):
    """
    A schema wraps a dictionary and defines a `uri`, `id`, and `type`.

    """
    @property
    def id(self):
        """
        The dictionary is assumed to have an "id" attribute.

        """
        return self["id"]

    @abstractproperty
    def embedded(self):
        pass

    @abstractmethod
    def links(self, follow_mode):
        pass

    @abstractproperty
    def parents(self):
        pass

    @abstractproperty
    def type(self):
        pass

    @abstractproperty
    def uri(self):
        pass
