"""

"""

from microcosm_resourcesync.resources.base import Resource


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
