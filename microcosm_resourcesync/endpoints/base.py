"""
Endpoint interface

"""
from abc import ABCMeta, abstractmethod
from six import add_metaclass

from microcosm_resourcesync.formatters import Formatters


@add_metaclass(ABCMeta)
class Endpoint(object):
    """
    An endpoint is able to read and write resources.

    """
    @property
    def default_formatter(self):
        return Formatters.YAML.name

    @abstractmethod
    def read(self, schema_cls, **kwargs):
        """
        Generate resource lists of the given class.

        """
        pass

    @abstractmethod
    def write(self, resources, formatter, **kwargs):
        """
        Write resources using the given formatter.

        """
        pass

    def validate_for_read(self, schema_cls, **kwargs):
        """
        Validate that reading is possible.

        """
        pass

    def validate_for_write(self, formatter, **kwargs):
        """
        Validate that writing is possible.

        """
        pass
