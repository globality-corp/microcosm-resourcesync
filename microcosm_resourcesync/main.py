"""
Command line entry points.

"""
from click import (
    argument,
    command,
    echo,
    option,
)

from microcosm_resourcesync.formatters import Formatters
from microcosm_resourcesync.resources import Resources


@command()
@option("--json", "-j", "formatter", flag_value=Formatters.JSON, help="Use json output")
@option("--yaml", "-y", "formatter", flag_value=Formatters.YAML, help="Use yaml output")
@option("--hal", "resource_type", flag_value=Resources.HAL, help="Use HAL JSON resources (default)")
@option("--simple", "resource_type", flag_value=Resources.SIMPLE, help="Use Simple JSON resources")
@argument("origin")
@argument("destination")
def main(formatter, resource_type, origin, destination):
    echo("Synchronizing resources from: {} to: {}".format(
        origin,
        destination,
    ))
