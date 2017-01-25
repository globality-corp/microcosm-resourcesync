"""
Command line entry points.

"""
from click import (
    argument,
    command,
    echo,
    option,
)


@command()
@option("--json", "-j", "formatter", flag_value="JSON", help="Use json output")
@option("--yaml", "-y", "formatter", flag_value="YAML", help="Use yaml output")
@argument("origin")
@argument("destination")
def main(formatter, origin, destination):
    echo("Synchronizing resources from: {} to: {}".format(
        origin,
        destination,
    ))
