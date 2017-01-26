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

    @property
    def show_progressbar(self):
        return False

    @abstractmethod
    def read(self, schema_cls, **kwargs):
        """
        Generate resources of the given schema.

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
