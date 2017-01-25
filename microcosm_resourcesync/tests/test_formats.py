"""
Format tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from microcosm_resourcesync.formats import Formats


EXAMPLE = dict(
    id="c7f12ba5885f4b47bfafaa583cd5a097",
    foo="bar",
)


def test_json():
    formatter = Formats.JSON.value
    assert_that(
        formatter.load(formatter.dump(EXAMPLE)),
        is_(equal_to(EXAMPLE)),
    )


def test_yaml():
    formatter = Formats.YAML.value
    assert_that(
        formatter.load(formatter.dump(EXAMPLE)),
        is_(equal_to(EXAMPLE)),
    )
