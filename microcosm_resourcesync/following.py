"""
Following controls.

"""
from enum import Enum, unique


@unique
class FollowMode(Enum):
    """
    Hypertext traversal mode.

     -  Follow all links (ALL)
     -  Follow child links (CHILD)
     -  Follow pagination only (PAGE)

    """
    ALL = u"ALL"
    CHILD = u"CHILD"
    PAGE = u"PAGE"
