"""

"""
from microcosm_resourcesync.schemas.base import Schema


class HALSchema(Schema):
    """
    A schema that implements HAL JSON linking.

    """
    @property
    def parents(self):
        for relation, links in self["_links"].items():
            if relation == "self" or relation.startswith("child:"):
                continue
            if isinstance(links, list):
                for link in links:
                    yield link["href"]
            else:
                link = links["href"]
                yield link

    @property
    def type(self):
        """
        We assume that the URI is of the form: `https://example.com/path/to/<type>/<id>`

        """
        return self.uri.split("/")[-2]

    @property
    def uri(self):
        """
        We assume that the resource has a valid HAL self link.

        """
        return self["_links"]["self"]["href"]
