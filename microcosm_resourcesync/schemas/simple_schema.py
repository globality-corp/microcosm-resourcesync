"""

"""

from microcosm_resourcesync.schemas.base import Schema


class SimpleSchema(Schema):
    """
    A schema that encodes uri/type verbatim in its dictionary.

    """
    @property
    def links(self):
        return self.get("links", [])

    @property
    def parents(self):
        return self.get("parents", [])

    @property
    def type(self):
        return self["type"]

    @property
    def uri(self):
        return self["uri"]
