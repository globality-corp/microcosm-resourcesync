"""
A schema using HAL JSON linking conventions.

"""
from microcosm_resourcesync.following import FollowMode
from microcosm_resourcesync.schemas.base import Link, Schema

HTTP_EXCLUDED_KEYS = ["id", "_links"]


class HALSchema(Schema):
    """
    A schema that implements HAL JSON linking.

    """
    def to_http_data(self):
        """
        We now use marshmallow 3, which means strict validation of input.
        Extra fields trigger 422 errors; there are some keys that we know will
        never be part of an input resource, remove them here.

        Note: the general solution would be to pass in a separate schema for every resource
        we deal with; this is a simpler fix that works with how we use `microcosm-resourcesync`
        in practice. It may not always work.

        """
        return {
            key: value
            for key, value in self.items()
            if key not in HTTP_EXCLUDED_KEYS
        }

    @property
    def embedded(self):
        return self.get("items", [])

    def links(self, follow_mode):
        return [
            Link(relation, uri)
            for relation, uri in self.iter_links()
            if self.should_follow(relation, uri, follow_mode)
        ]

    @property
    def parents(self):
        return [
            uri
            for relation, uri in self.iter_links()
            if relation.startswith("parent:")
        ]

    def should_follow(self, relation, uri, follow_mode):
        """
        Compute whether a link should be followed.

        We use the convention that a link prefixed with "child:" is a non-parent link.

        """
        if follow_mode == FollowMode.NONE:
            return False

        if relation == "self":
            # don't follow self links
            return False

        if follow_mode == FollowMode.ALL:
            return True

        if follow_mode == FollowMode.CHILD and relation.startswith("child:"):
            return True

        if follow_mode in (FollowMode.CHILD, FollowMode.PAGE) and relation in ("next", "prev"):
            return True

        return False

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
