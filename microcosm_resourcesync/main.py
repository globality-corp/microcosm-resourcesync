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
from microcosm_resourcesync.options import Options
from microcosm_resourcesync.schemas import Schemas


def validate_endpoint(context, param, value):
    try:
        return endpoint_for(value)
    except:
        raise BadParameter("Unsupported endpoint format: {}".format(value))


def validate_positive(context, param, value):
    if value < 1:
        raise BadParameter("Must be positive")
    return value


def batched(resources, batch_size):
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
def main(context,
         formatter,
         resource_type,
         remove,
         follow,
         batch_size,
         max_attempts,
         origin,
         destination):
    """
    Synchronized resources from origin endpoint to destination endpoint.

    """
    if origin == destination:
        context.fail("origin and destination may not be the same")

    options = Options(
        batch_size=batch_size,
        formatter=Formatters[formatter or destination.default_formatter],
        max_attempts=max_attempts,
        remove=remove,
        schema_cls=Schemas[resource_type or Schemas.HAL.name].value,
    )
    options_kwargs = vars(options)

    origin.validate_for_read(**options_kwargs)
    destination.validate_for_write(**options_kwargs)

    echo("Reading resources from: {}".format(origin), err=True)
    resources = list(origin.read(**options_kwargs))

    # XXX toposort

    echo("Writing resources to: {}".format(destination), err=True)
    progress_file = stderr if destination.show_progressbar else NullIO()
    with progressbar(length=len(resources), file=progress_file) as progressbar_:
        for resource_batch in batched(resources, options.batch_size):
            destination.write(resources, **options_kwargs)
            progressbar_.update(len(resource_batch))
