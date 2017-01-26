"""

"""
from microcosm_resourcesync.schemas.base import Schema


class HALSchema(Schema):
    """
    A schema that implements HAL JSON linking.

    """
    @property
    def links(self):
        return [
            uri
            for relation, uri in self.iter_links()
        ]

    @property
    def parents(self):
        """
        Compute parent URIs using link hypertext.

        We use the convention that a link prefixed with "child:" is a non-parent link.

        """
        return [
            uri
            for relation, uri in self.iter_links()
            if relation != "self" and not relation.startswith("child:")
        ]

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

    def iter_links(self):
        for relation, links in self["_links"].items():
            if isinstance(links, list):
                for link in links:
                    yield relation, link["href"]
            else:
                link = links["href"]
                yield relation, link
