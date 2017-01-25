"""
Supported formatters

"""
from enum import Enum, unique


from microcosm_resourcesync.formatters.json_formatter import JSONFormatter
from microcosm_resourcesync.formatters.yaml_formatter import YAMLFormatter


@unique
class Formatters(Enum):
    JSON = JSONFormatter()
    YAML = YAMLFormatter()
