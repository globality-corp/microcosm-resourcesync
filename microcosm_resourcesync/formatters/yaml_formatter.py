"""
YAML Formatter

"""
from yaml import safe_dump, safe_load

from microcosm_resourcesync.formatters.base import Formatter


class YAMLFormatter(Formatter):

    def load(self, data):
        return safe_load(data)

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