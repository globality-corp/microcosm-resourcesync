"""
Supported resource formats.

"""
from abc import ABCMeta, abstractmethod
from enum import Enum, unique
from json import dumps as dump_json, loads as load_json
from six import add_metaclass

from yaml import safe_dump as dump_yaml, safe_load as load_yaml


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


class JSONFormatter(Formatter):

    def load(self, data):
        return load_json(data)

    def dump(self, dct):
        return dump_json(dct)


class YAMLFormatter(Formatter):

    def load(self, data):
        return load_yaml(data)

    def dump(self, dct):
        return dump_yaml(
            dict(dct),
            # show every document in its own block
            default_flow_style=False,
            # start a new document (via "---") before every resource
            explicit_start=True,
            # follow (modern) PEP8 max line length and indent
            width=99,
            indent=4,
        )


@unique
class Formatters(Enum):
    JSON = JSONFormatter()
    YAML = YAMLFormatter()
