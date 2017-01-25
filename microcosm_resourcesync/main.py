"""
Command line entry points.

"""
from click import (
    argument,
    BadParameter,
    Choice,
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
@option("--json", "-j", "formatter", flag_value=Formatters.JSON.name, help="Use json output")
@option("--yaml", "-y", "formatter", flag_value=Formatters.YAML.name, help="Use yaml output")
@option("--hal", "resource_type", flag_value=Resources.HAL.name, help="Use HAL JSON resources (default)")
@option("--simple", "resource_type", flag_value=Resources.SIMPLE.name, help="Use Simple JSON resources")
@option("--rm", "remove", is_flag=True)
@option("--follow", is_flag=True)
@argument("origin", callback=validate_endpoint)
@argument("destination", callback=validate_endpoint)
def main(context,
         formatter,
         resource_type,
         remove,
         follow,
         origin,
         destination):
    """
    Synchronized resources from origin endpoint to destination endpoint.

    """
    if origin == destination:
        context.fail("origin and destination may not be the same")

    resource_cls = Resources[resource_type or Resources.HAL.name].value
    formatter = Formatters[formatter or destination.default_formatter]

    origin.validate_for_read(
        resource_cls,
        follow=follow,
    )
    destination.validate_for_write(
        formatter=formatter,
        remove=remove,
    )

    echo("Synchronizing resources from: {} to: {}".format(
        origin,
        destination,
    ))

    for resources in origin.read(resource_cls, follow=follow):
        # XXX batching, deduplication, sorting
        destination.write(
            resources,
            formatter=formatter,
            remove=remove,
        )
