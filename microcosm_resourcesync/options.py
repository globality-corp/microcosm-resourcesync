"""
CLI Options.

"""
from collections import namedtuple


Options = namedtuple(
    "Options",
    [
        "batch_size",
        "formatter",
        "max_attempts",
        "remove",
        "schema_cls",
    ],
)
