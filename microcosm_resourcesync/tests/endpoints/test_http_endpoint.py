"""
HTTP Endpoint tests

"""
from json import dumps
from unittest.mock import Mock, patch

from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_,
)

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


class TestHTTPEndpoint:

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
                auth=None,
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

        with patch.object(self.endpoint.session, "options") as mocked_options:
            mocked_options.return_value.status_code == 200
            mocked_options.return_value.headers = dict(
                Allow=["HEAD", "POST", "OPTIONS", "GET", "PATCH"],
            )
            with patch.object(self.endpoint.session, "patch") as mocked_patch:
                self.endpoint.write(
                    resources=resources,
                    batch_size=2,
                    formatter=Formatters.JSON,
                    max_attempts=1,
                )

        assert_that(mocked_patch.call_count, is_(equal_to(2)))
        mocked_patch.assert_any_call(
            "http://example.com/api/foo",
            auth=None,
            data=Formatters.JSON.value.dump(dict(
                items=resources[0:2],
            )),
            headers={'Content-Type': 'application/json'}
        )
        mocked_patch.assert_any_call(
            "http://example.com/api/foo",
            auth=None,
            data=Formatters.JSON.value.dump(dict(
                items=resources[2:],
            )),
            headers={'Content-Type': 'application/json'}
        )

    def test_write_batch_not_supported(self):
        resources = [
            HALSchema(hal_resource("http://example.com/api/foo/1")),
            HALSchema(hal_resource("http://example.com/api/foo/2")),
            HALSchema(hal_resource("http://example.com/api/foo/3")),
            HALSchema(hal_resource("http://example.com/api/foo/4")),
        ]

        with patch.object(self.endpoint.session, "options") as mocked_options:
            mocked_options.return_value.status_code == 200
            mocked_options.return_value.headers = dict(
                Allow=["HEAD", "POST", "OPTIONS", "GET"],
            )
            with patch.object(self.endpoint.session, "patch") as mocked_patch:
                with patch.object(self.endpoint.session, "put") as mocked_put:
                    self.endpoint.write(
                        resources=resources,
                        batch_size=2,
                        formatter=Formatters.JSON,
                        max_attempts=1,
                    )

        # NB: only call options once because we are caching
        assert_that(mocked_options.call_count, is_(equal_to(1)))
        assert_that(mocked_patch.call_count, is_(equal_to(0)))
        assert_that(mocked_put.call_count, is_(equal_to(4)))
