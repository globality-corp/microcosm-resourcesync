# microcosm-resourcesync

Synchronize resources between endpoints

In non-trivial deployments of RESTful services, it is common to have multiple copies of the same service
running in different environments (development, testing, staging, production, etc). In many cases, it is
useful to synchronize some resource data between environments by first copying content to an intermediate
format and then copying that format to another environment.

This process is especially useful if the intermediate format lives in version control and supports diffs
and merging well.


## Main Use Cases

 1. Pull data from an HTTP endpoint to a local directory:

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

    The destination argument may also be a `.yaml` file path, in which case a single file will be generated.

 2. Push data from a local directory to an HTTP (base) url:

        resource-sync /path/to/local/data https://example.com

    In this case, `resource-sync` will push the local resource(s) to the remote server. By default, each resource
    will be encoded using JSON, though YAML may be used instead via the `--yaml` flag.

    If the resources define dependency relationships, a *topological* sort will be used to ensure that resources
    are pushed in the correct order (e.g. assuming a remote server with no prior content).

 3. Replacing existing resource content with new content.


## Basic Assumptions

`resource-sync` makes the following assumptions about HTTP and resources:

 1. Resources are encoded in either JSON or YAML.
 2. Resources have a globally uniquely `URI`
 3. Resources have a `type`
 4. Resources have a type-specific `id`
 5. Resources can be retrieved by using the HTTP `GET` operation against this URI
 6. Resources can be replaced by using the HTTP `PUT` operation against this URI
 7. Resources have the same URI path in every environment (but with different URI bases)

By default, `resource-sync` also supports the [HAL JSON](http://stateless.co/hal_specification.html) model
for JSON-based hypertext. For resources that define hypertext, the `self` link will be used as the resource's canonical
URI (even if some other URI was used to retrieve it) and other links may be used to define dependency relationships.


## TODO

 -  Selectively ignoring some resources
 -  Updating resources in batches
 -  Deletion from HTTP endpoints
