"""
Test batching.

"""
from hamcrest import assert_that, contains

from microcosm_resourcesync.batching import batched
from microcosm_resourcesync.schemas import SimpleSchema


resources = [
    SimpleSchema(
        id=1,
        type="foo",
        uri="http://example.com/foo/1",
    ),
    SimpleSchema(
        id=1,
        type="bar",
        uri="http://example.com/bar/1",
    ),
    SimpleSchema(
        id=2,
        type="bar",
        uri="http://example.com/bar/2",
    ),
    SimpleSchema(
        id=3,
        type="bar",
        uri="http://example.com/bar/3",
    ),
    SimpleSchema(
        id=2,
        type="foo",
        uri="http://example.com/foo/2",
    ),
]


def test_batching_size_one():
    assert_that(
        list(batched(resources, batch_size=1)),
        contains(
            resources[0:1],
            resources[1:2],
            resources[2:3],
            resources[3:4],
            resources[4:],
        )
    )


def test_batching_size_two():
    assert_that(
        list(batched(resources, batch_size=2)),
        contains(
            resources[0:1],
            resources[1:3],
            resources[3:4],
            resources[4:],
        )
    )


def test_batching_size_three():
    assert_that(
        list(batched(resources, batch_size=3)),
        contains(
            resources[0:1],
            resources[1:4],
            resources[4:],
        )
    )
