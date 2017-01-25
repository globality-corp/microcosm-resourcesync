"""
Endpoint types.

"""
from microcosm_resourcesync.endpoints.http_endpoint import HTTPEndpoint
from microcosm_resourcesync.endpoints.pipe_endpoint import PipeEndpoint
from microcosm_resourcesync.endpoints.yaml_file_endpoint import YAMLFileEndpoint


def endpoint_for(endpoint):
    """
    Interpret endpoint as correct type.

    """
    if endpoint == "-":
        return PipeEndpoint()

    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return HTTPEndpoint(endpoint)

    if endpoint.endswith(".yaml") or endpoint.endswith(".yml"):
        return YAMLFileEndpoint(endpoint)

    raise Exception
