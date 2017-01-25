"""
Resource tests.

"""
from microcosm_resourcesync.resources import (
    HALResource,
    SimpleResource,
)


from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

ID = "c7f12ba5885f4b47bfafaa583cd5a097"
TYPE = "foo"
URI = "http://example.com/{}/{}".format(TYPE, ID)

HAL_EXAMPLE = dict(
    id=ID,
    _links=dict(
        self=dict(
            href=URI
        ),
    ),
)


SIMPLE_EXAMPLE = dict(
    id=ID,
    type=TYPE,
    uri=URI,
)


def test_hal_resource():
    resource = HALResource(HAL_EXAMPLE)
    assert_that(resource.id, is_(equal_to(ID)))
    assert_that(resource.type, is_(equal_to(TYPE)))
    assert_that(resource.uri, is_(equal_to(URI)))


def test_simple_resource():
    resource = SimpleResource(SIMPLE_EXAMPLE)
    assert_that(resource.id, is_(equal_to(ID)))
    assert_that(resource.type, is_(equal_to(TYPE)))
    assert_that(resource.uri, is_(equal_to(URI)))
