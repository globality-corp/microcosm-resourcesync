# microcosm-resourcesync

Synchronize resources between endpoints

In non-trivial deployments of RESTful services, it is common to have multiple copies of the same service
running in different environments (development, testing, staging, production, etc). In many cases, it is
useful to synchronize some resource data between environments by first copying content to an intermediate
format and then copying that format to another environment.

This process is especially useful if the intermediate format lives in version control and supports diffs
and merging well.


## Usage

The main usage is synchronizes from an `origin` endpoint to a `destination` endpoint:

    resource-sync <origin> <destination>

Where endpoints may be any of the following:

 -  An HTTP(s) URL
 -  A YAML file
 -  A directory path
 -  The literal `-` (for `stdin`/`stdout`)


## Formatting

Resources are assumed to be formatted as either JSON or YAML.

Origin endpoints define their own format and destination endpoints define a *default* format; the latter can be
overridden on the command line using `--json` or `--yaml`.


## Representation

Each resources is expected to define a minimal set of attributes. (See also `Assumptions`, below).

In order to extract these attributes from the resource data (after formatting), a schema needs to be applied. The
default behavior assumes that resources use [HAL JSON](http://stateless.co/hal_specification.html) to define
hypertext. An alternate, simple schema can also be selected using `--simple` (vs `--hal`).


## Capturing Data

A common use case is pull data from an HTTP endpoint to a local directory:

    resource-sync https://example.com/foo /path/to/local/data

The HTTP response may contain multiple resources (especially for endpoints implementing the microcosm
[Search](https://github.com/globality-corp/microcosm-flask/blob/develop/microcosm_flask/operations.py#L33)
convention or some other form of pagination). Similarly, the `--follow/--no-follow` flags can be used to
control whether `resource-sync` traverses hypertext ("links") present in the HTTP response and pulls
further resources.

Each resource captured from the HTTP endpoint will be saved into its own file within the directory tree,
using type-specific sub-directories. By default, each resource will be stored as YAML (for better human
readability), though JSON may be used instead via the `--json` flag.

For directory trees that live in version control, the `--rm` flag can be used to first remove all existing
data before syncronizing, thereby creating a full diff.


## Replaying Data

Another common use case is push data from a local directory to an HTTP endpoint:

    resource-sync /path/to/local/data https://example.com

In this case, `resource-sync` will push the local resource(s) to the remote server.

If the resources define dependency relationships, a *topological* sort will be used to ensure that resources
are pushed in the correct order (e.g. assuming a remote server with no prior content).


## Assumptions

`resource-sync` makes the following assumptions about HTTP and resources:

 1. Resources are encoded in either JSON or YAML.
 2. Resources have a globally uniquely `URI`
 3. Resources have a `type`
 4. Resources have a type-specific `id`
 5. Resources can be retrieved by using the HTTP `GET` operation against this URI
 6. Resources can be replaced by using the HTTP `PUT` operation against this URI
 7. Resources have the same URI path in every environment (but with different URI bases)


## TODO

 -  Updating resources in batches
 -  Deletion from HTTP endpoints
