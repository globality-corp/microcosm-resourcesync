"""
HTTP endpoint.

"""
from six.moves.urllib.parse import urlparse, urlunparse

from requests import Session

from microcosm_resourcesync.endpoints.base import Endpoint
from microcosm_resourcesync.formatters import Formatters


class HTTPEndpoint(Endpoint):
    """
    Read and write resources for an HTTP URI.

    """
    def __init__(self, uri):
        self.uri = uri
        self.session = Session()

    def __repr__(self):
        return "{}('{}')".format(
            self.__class__.__name__,
            self.uri,
        )

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.uri == other.uri

    @property
    def default_formatter(self):
        return Formatters.JSON.name

    def read(self, schema_cls, **kwargs):
        """
        Read all YAML documents from the file.

        """
        response = self.session.get(self.uri)
        response.raise_for_status()

        content_type = response.headers["Content-Type"]
        formatter = Formatters.for_content_type(content_type).value

        yield [schema_cls(formatter.load(response.text))]

    def write(self, resources, formatter, **kwargs):
        """
        Write resources as YAML to the file.

        """
        # XXX batching
        # XXX error handling, retry, logging (and verbosity)
        for resource in resources:
            uri = self.join_uri(resource.uri)
            data = formatter.value.dump(resource)
            response = self.session.put(
                uri,
                data=data,
                headers={
                    "Content-Type": formatter.value.preferred_mime_type,
                },
            )
            response.raise_for_status()

    def join_uri(self, uri):
        """
        Construct a URL using the configured base URL's scheme and netloc and the remainder of the resource's URI.

        This is what `urljoin` ought to do...

        """
        parsed_base_uri = urlparse(self.uri)
        parsed_uri = urlparse(uri)
        return urlunparse(parsed_uri._replace(
            scheme=parsed_base_uri.scheme,
            netloc=parsed_base_uri.netloc,
        ))
