"""
Resource modeling.

"""
from abc import ABCMeta, abstractproperty
from enum import Enum, unique
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


class SimpleResource(Resource):
    """
    A resource that encodes uri/type verbatim in its dictionary.

    """
    @property
    def type(self):
        return self["type"]

    @property
    def uri(self):
        return self["uri"]


class HALResource(Resource):
    """
    A resource that implements HAL JSON linking.

    """
    @property
    def type(self):
        """
        We assume that the URI is of the form: `https://example.com/path/to/<type>/<id>`

        """
        return self.uri.split("/")[-2]

    @property
    def uri(self):
        """
        We assume that the resource has a valid HAL self link.

        """
        return self["_links"]["self"]["href"]


@unique
class Resources(Enum):
    HAL = HALResource
    SIMPLE = SimpleResource
