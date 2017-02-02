"""
HTTP Endpoint tests

"""
from json import dumps

from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_,
)
from mock import patch, Mock

from microcosm_resourcesync.endpoints import HTTPEndpoint
from microcosm_resourcesync.following import FollowMode
from microcosm_resourcesync.formatters import Formatters
from microcosm_resourcesync.schemas import HALSchema


def hal_resource(href):
    return dict(
        _links=dict(
            self=dict(
                href=href,
            ),
        ),
        id=href.split("/")[-1],
    )


def merged(dct, **kwargs):
    dct.update(**kwargs)
    return dct


def linked(dct, **kwargs):
    dct["_links"].update(**kwargs)
    return dct


def set_response(mock, *resources):
    mock.side_effect = [
        Mock(
            headers={
                "Content-Type": "application/json",
            },
            text=dumps(resource),
        )
        for resource in resources
    ]


class TestHTTPEndpoint(object):

    def setup(self):
        self.uri = "http://example.com/api"
        self.endpoint = HTTPEndpoint(self.uri)

    def test_read_follow_none(self):
        with patch.object(self.endpoint.session, "get") as mocked_get:
            set_response(
                mocked_get,
                hal_resource("http://example.com/api/foo/1"),
            )
            resources = list(self.endpoint.read(
                schema_cls=HALSchema,
                follow_mode=FollowMode.NONE,
                verbose=False,
                limit=10,
            ))

        assert_that(resources, has_length(1))
        assert_that(resources[0].id, is_(equal_to("1")))

    def test_read_follow_none_embedded(self):
        with patch.object(self.endpoint.session, "get") as mocked_get:
            set_response(
                mocked_get,
                merged(
                    hal_resource("http://example.com/api/foo/1"),
                    items=[
                        hal_resource("http://example/com/api/bar/1"),
                        hal_resource("http://example/com/api/bar/2"),
                    ],
                ),
            )
            resources = list(self.endpoint.read(
                schema_cls=HALSchema,
                follow_mode=FollowMode.CHILD,
                verbose=False,
                limit=10,
            ))

        assert_that(resources, has_length(3))
        assert_that(resources[0].id, is_(equal_to("1")))

    def test_read_follow_child(self):
        with patch.object(self.endpoint.session, "get") as mocked_get:
            set_response(
                mocked_get,
                linked(
                    hal_resource("http://example.com/api/foo/1"),
                    **{
                        "child:bar": dict(
                            href="http://example.com/api/bar/1",
                        ),
                    }
                ),
                hal_resource("http://example.com/api/bar/1"),
            )
            resources = list(self.endpoint.read(
                schema_cls=HALSchema,
                follow_mode=FollowMode.CHILD,
                verbose=False,
                limit=10,
            ))

        assert_that(resources, has_length(2))
        assert_that(resources[0].type, is_(equal_to("foo")))
        assert_that(resources[1].type, is_(equal_to("bar")))

    def test_read_follow_page(self):
        with patch.object(self.endpoint.session, "get") as mocked_get:
            set_response(
                mocked_get,
                dict(
                    _links=dict(
                        self=dict(
                            href="http://example.com/api/foo?offset=0&limit2",
                        ),
                        next=dict(
                            href="http://example.com/api/foo?offset=2&limit=2",
                        ),
                    ),
                    items=[
                        hal_resource("http://example.com/api/foo/1"),
                        hal_resource("http://example.com/api/foo/2"),
                    ],
                ),
                dict(
                    _links=dict(
                        self=dict(
                            href="http://example.com/api/foo?offset=2&limit2",
                        ),
                        prev=dict(
                            href="http://example.com/api/foo?offset=0&limit=2",
                        ),
                    ),
                    items=[
                        hal_resource("http://example.com/api/foo/3"),
                        hal_resource("http://example.com/api/foo/4"),
                    ],
                ),

            )
            resources = list(self.endpoint.read(
                schema_cls=HALSchema,
                follow_mode=FollowMode.PAGE,
                verbose=False,
                limit=10,
            ))

        assert_that(resources, has_length(4))
        assert_that(resources[0].id, is_(equal_to("1")))
        assert_that(resources[1].id, is_(equal_to("2")))
        assert_that(resources[2].id, is_(equal_to("3")))
        assert_that(resources[3].id, is_(equal_to("4")))

    def test_write(self):
        resources = [
            HALSchema(hal_resource("http://example.com/api/foo/1")),
            HALSchema(hal_resource("http://example.com/api/foo/2")),
            HALSchema(hal_resource("http://example.com/api/foo/3")),
            HALSchema(hal_resource("http://example.com/api/foo/4")),
        ]

        with patch.object(self.endpoint.session, "put") as mocked_put:
            self.endpoint.write(
                resources=resources,
                batch_size=1,
                formatter=Formatters.JSON,
                max_attempts=1,
            )

        assert_that(mocked_put.call_count, is_(equal_to(4)))
        for resource in resources:
            mocked_put.assert_any_call(
                resource.uri,
                data=Formatters.JSON.value.dump(resource),
                headers={'Content-Type': 'application/json'}
            )

    def test_write_batch(self):
        resources = [
            HALSchema(hal_resource("http://example.com/api/foo/1")),
            HALSchema(hal_resource("http://example.com/api/foo/2")),
            HALSchema(hal_resource("http://example.com/api/foo/3")),
            HALSchema(hal_resource("http://example.com/api/foo/4")),
        ]

        with patch.object(self.endpoint.session, "put") as mocked_put:
            self.endpoint.write(
                resources=resources,
                batch_size=2,
                formatter=Formatters.JSON,
                max_attempts=1,
            )

        assert_that(mocked_put.call_count, is_(equal_to(4)))
        for resource in resources:
            mocked_put.assert_any_call(
                resource.uri,
                data=Formatters.JSON.value.dump(resource),
                headers={'Content-Type': 'application/json'}
            )
