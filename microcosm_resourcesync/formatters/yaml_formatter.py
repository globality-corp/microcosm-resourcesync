"""
YAML Formatter

"""
from yaml import load, safe_dump
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from microcosm_resourcesync.formatters.base import Formatter


class YAMLFormatter(Formatter):

    def load(self, data):
        return load(data, Loader=SafeLoader)

    def dump(self, dct):
        return safe_dump(
            dict(dct),
            # show every document in its own block
            default_flow_style=False,
            # start a new document (via "---") before every resource
            explicit_start=True,
            # follow (modern) PEP8 max line length and indent
            width=99,
            indent=4,
        )

    @property
    def extension(self):
        return ".yaml"

    @property
    def mime_types(self):
        return [
            "application/yaml",
            "application/x-yaml",
            "text/vnd.yaml",
            "text/yaml",
            "text/x-yaml",
        ]
