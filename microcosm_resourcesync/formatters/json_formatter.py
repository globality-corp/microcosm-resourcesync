"""
JSON Formatter

"""
from json import dumps, loads

from microcosm_resourcesync.formatters.base import Formatter


class JSONFormatter(Formatter):

    def load(self, data):
        return loads(data)

    def dump(self, dct):
        return dumps(dct)
