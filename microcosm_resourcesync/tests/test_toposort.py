"""
Toposort test.

"""
from hamcrest import (
    assert_that,
    contains,
)

from microcosm_resourcesync.schemas import SimpleSchema
from microcosm_resourcesync.toposort import toposorted


resources = [
    SimpleSchema(
        id=1,
        type="foo",
        uri="http://example.com/foo/1",
    ),
    SimpleSchema(
        id=2,
        type="foo",
        uri="http://example.com/foo/2",
        parents=[
            "http://example.com/foo/1",
        ],
    ),
    SimpleSchema(
        id=3,
        type="foo",
        uri="http://example.com/foo/3",
    ),
    SimpleSchema(
        id=1,
        type="bar",
        uri="http://example.com/bar/1",
        parents=[
            "http://example.com/foo/1",
        ],
    ),
]


def test_toposort():
    assert_that(
        toposorted(resources),
        contains(
            resources[2],
            resources[0],
            resources[1],
            resources[3],
        ),
    )
