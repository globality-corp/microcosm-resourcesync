"""
Command line entry points.

"""
from click import (
    argument,
    BadParameter,
    command,
    echo,
    option,
    pass_context,
)

from microcosm_resourcesync.endpoints import endpoint_for
from microcosm_resourcesync.formatters import Formatters
from microcosm_resourcesync.resources import Resources


def validate_endpoint(context, param, value):
    try:
        return endpoint_for(value)
    except:
        raise BadParameter("Unsupported endpoint format: {}".format(value))


@command()
@pass_context
@option("--json", "-j", "formatter", flag_value=Formatters.JSON, help="Use json output")
@option("--yaml", "-y", "formatter", flag_value=Formatters.YAML, help="Use yaml output")
@option("--hal", "resource_type", flag_value=Resources.HAL, help="Use HAL JSON resources (default)")
@option("--simple", "resource_type", flag_value=Resources.SIMPLE, help="Use Simple JSON resources")
@option("--rm", "remove_first", is_flag=True)
@argument("origin", callback=validate_endpoint)
@argument("destination", callback=validate_endpoint)
def main(context, formatter, remove_first, resource_type, origin, destination):
    """
    Synchronized resources from origin endpoint to destination endpoint.

    """
    if origin == destination:
        context.fail("origin and destination may not be the same")

    if resource_type:
        resource_cls = Resources(resource_type).value
    else:
        resource_cls = Resources.HAL.value

    formatter = formatter or Formatters.YAML

    origin.validate_for_read(resource_cls)
    destination.validate_for_write(formatter, remove_first)

    echo("Synchronizing resources from: {} to: {}".format(
        origin,
        destination,
    ))

    for resources in origin.read(resource_cls):
        # XXX batching, deduplication, sorting
        destination.write(resources, formatter, remove_first)
