"""
HTTP endpoint.

"""
from six.moves.urllib.parse import urlparse, urlunparse

from click import echo
from requests import Session
from requests.exceptions import ConnectionError, HTTPError

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

    @property
    def show_progressbar(self):
        return True

    def read(self, schema_cls, **kwargs):
        """
        Read all YAML documents from the file.

        """
        response = self.session.get(self.uri)
        response.raise_for_status()

        content_type = response.headers["Content-Type"]
        formatter = Formatters.for_content_type(content_type).value

        resource = schema_cls(formatter.load(response.text))

        if hasattr(resource, "id"):
            yield resource

        for child in resource.get("items", []):
            yield schema_cls(child)

    def write(self, resources, formatter, batch_size, max_attempts, **kwargs):
        """
        Write resources as YAML to an HTTP endpoint.

        NB: we currently ignore the batch size, but we should adopt the BulkUpdate convention
        for batches of size greater than one.

        """
        for resource in resources:
            uri = self.join_uri(resource.uri)
            data = formatter.value.dump(resource)
            response = self.retry(
                self.session.put,
                uri=uri,
                data=data,
                headers={
                    "Content-Type": formatter.value.preferred_mime_type,
                },
                max_attempts=max_attempts,
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

    def retry(self, func, uri, max_attempts, **kwargs):
        """
        Retry HTTP operations on connection failures.

        """
        last_error = None
        for attempt in range(max_attempts):
            try:
                return func(uri, **kwargs)
            except ConnectionError as error:
                echo("Connection error for uri: {}: {}".format(uri, error), err=True)
                last_error = error
                continue
            except HTTPError as error:
                if error.response.status_code in (504, 502):
                    echo("HTTP error for uri: {}: {}".format(uri, error), err=True)
                    last_error = error
                    continue
                raise
            else:
                break
        else:
            # If we reached here, all attempts were unsuccessful - raise last error encountered
            raise last_error
