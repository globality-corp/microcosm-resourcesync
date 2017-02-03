"""
Toposort test.

"""
from random import shuffle

from hamcrest import (
    assert_that,
    contains,
)

from microcosm_resourcesync.schemas import SimpleSchema
from microcosm_resourcesync.toposort import toposorted


resources = [
    SimpleSchema(
        id=1,
        type="parent",
        uri="http://example.com/parent/1",
    ),
    SimpleSchema(
        id=2,
        type="child",
        uri="http://example.com/child/2",
        parents=[
            "http://example.com/parent/1",
        ],
    ),
    SimpleSchema(
        id=3,
        type="grandchild",
        uri="http://example.com/grandchild/3",
        parents=[
            "http://example.com/child/2",
        ],
    ),
    SimpleSchema(
        id=4,
        type="grandchild",
        uri="http://example.com/grandchild/4",
        parents=[
            "http://example.com/child/2",
        ],
    ),
    SimpleSchema(
        id=5,
        type="child",
        uri="http://example.com/child/5",
        parents=[
            "http://example.com/parent/1",
        ],
    ),
    SimpleSchema(
        id=6,
        type="grandchild",
        uri="http://example.com/grandchild/6",
        parents=[
            "http://example.com/child/5",
        ],
    ),
    SimpleSchema(
        id=7,
        type="grandchild",
        uri="http://example.com/grandchild/7",
        parents=[
            "http://example.com/child/5",
        ],
    ),
]


def shuffled(lst):
    """
    Copy and shuffle.

    """
    result = list(lst)
    shuffle(result)
    return result


def test_toposort():
    assert_that(
        toposorted(shuffled(resources)),
        contains(
            resources[0],
            resources[1],
            resources[4],
            resources[2],
            resources[3],
            resources[5],
            resources[6],
        ),
    )
