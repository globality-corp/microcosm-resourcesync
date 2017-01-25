"""
Endpoint types.

"""
from abc import ABCMeta, abstractmethod
from six import add_metaclass
from os import makedirs, unlink
from os.path import dirname, exists

from click import ClickException
from yaml import safe_load_all

from microcosm_resourcesync.formatters import Formatters


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

    @staticmethod
    def for_(endpoint):
        if endpoint.endswith(".yaml") or endpoint.endswith(".yml"):
            return YAMLFileEndpoint(endpoint)
        raise Exception


class YAMLFileEndpoint(Endpoint):
    """
    Read and write resources for a single YAML file.

    For small data sizes, using a single YAML file results in a well-encapsulated,
    human-readable endpoint. For large data sizes, a directory endpoint is recommended instead.

    """
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return "{}('{}')".format(
            self.__class__.__name__,
            self.path,
        )

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.path == other.path

    def read(self, resource_cls):
        """
        Read all YAML documents from the file.

        """
        with open(self.path) as file_:
            raw_resources = safe_load_all(file_)

            for raw_resource in raw_resources:
                yield [resource_cls(raw_resource)]

    def write(self, resources, formatter, remove_first):
        """
        Write resources as YAML to the file.

        """
        with open(self.path, "a") as file_:
            for resource in resources:
                file_.write(formatter.value.dump(resource))

    def validate_for_write(self, formatter, remove_first):
        # must use the correct formatter (JSON doesn't support multi-document files)
        if formatter != Formatters.YAML:
            raise ClickException("Cannot use {} format YAMLFileEndpoint".format(
                formatter.name
            ))

        # handle existing files
        if exists(self.path):
            if remove_first:
                # remove
                unlink(self.path)
            else:
                raise ClickException("File already exists: {}; perhaps you mean to use '--rm'?".format(
                    self.path,
                ))

        # create directories
        try:
            makedirs(dirname(self.path))
        except OSError:
            pass
