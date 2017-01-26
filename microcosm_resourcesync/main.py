"""
Command line entry points.

"""
from sys import stderr

from click import (
    argument,
    BadParameter,
    command,
    echo,
    option,
    pass_context,
    progressbar,
)

from microcosm_resourcesync.endpoints import endpoint_for
from microcosm_resourcesync.formatters import Formatters
from microcosm_resourcesync.schemas import Schemas
from microcosm_resourcesync.toposort import toposorted


def validate_endpoint(context, param, value):
    try:
        return endpoint_for(value)
    except:
        raise BadParameter("Unsupported endpoint format: {}".format(value))


def validate_positive(context, param, value):
    if value < 1:
        raise BadParameter("Must be positive")
    return value


def batched(resources, batch_size, **kwargs):
    """
    Chunk resources into batches.

    """
    batch = []
    for resource in resources:
        batch.append(resource)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


class NullIO(object):
    def write(self, *args, **kwargs):
        pass

    def flush(self):
        pass


def sync(origin, destination, **kwargs):
    """
    Synchronize data from one endpoint to another.

    """
    origin.validate_for_read(**kwargs)
    destination.validate_for_write(**kwargs)

    echo("Reading resources from: {}".format(origin), err=True)
    resources = list(origin.read(**kwargs))

    echo("Toposorting {} resources".format(len(resources)), err=True)
    sorted_resources = toposorted(resources)

    echo("Writing resources to: {}".format(destination), err=True)
    progress_file = stderr if destination.show_progressbar else NullIO()
    with progressbar(length=len(resources), file=progress_file) as progressbar_:
        for resource_batch in batched(sorted_resources, **kwargs):
            destination.write(resource_batch, **kwargs)
            progressbar_.update(len(resource_batch))


@command()
@pass_context
@option("--json", "-j", "formatter", flag_value=Formatters.JSON.name, help="Use json output")
@option("--yaml", "-y", "formatter", flag_value=Formatters.YAML.name, help="Use yaml output")
@option("--hal", "resource_type", flag_value=Schemas.HAL.name, help="Use HAL JSON schema (default)")
@option("--simple", "resource_type", flag_value=Schemas.SIMPLE.name, help="Use Simple JSON schema")
@option("--rm", "remove", is_flag=True)
@option("--follow", is_flag=True)
@option("--batch-size", "-b", type=int, default=1, callback=validate_positive)
@option("--max-attempts", "-b", type=int, default=1, callback=validate_positive)
@argument("origin", callback=validate_endpoint)
@argument("destination", callback=validate_endpoint)
def main(context, origin, destination, formatter, resource_type, **kwargs):
    """
    Synchronized resources from origin endpoint to destination endpoint.

    """
    if origin == destination:
        context.fail("origin and destination may not be the same")

    formatter = Formatters[formatter or destination.default_formatter]
    schema_cls = Schemas[resource_type or Schemas.HAL.name].value

    sync(origin, destination, formatter=formatter, schema_cls=schema_cls, **kwargs)
