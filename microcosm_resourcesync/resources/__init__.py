"""
Resource modeling.

"""
from enum import Enum, unique

from microcosm_resourcesync.resources.hal_resource import HALResource
from microcosm_resourcesync.resources.simple_resource import SimpleResource


@unique
class Resources(Enum):
    HAL = HALResource
    SIMPLE = SimpleResource
