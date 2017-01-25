"""
Endpoint types.

"""
from microcosm_resourcesync.endpoints.yaml_file_endpoint import YAMLFileEndpoint


def endpoint_for(endpoint):
    if endpoint.endswith(".yaml") or endpoint.endswith(".yml"):
        return YAMLFileEndpoint(endpoint)
        raise Exception
