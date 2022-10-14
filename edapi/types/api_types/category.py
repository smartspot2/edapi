"""
Category type usd in the Ed API.

There are two versions; a recursive version and a non-recursive version.
"""

from typing import Optional, TypedDict

from .content import ContentString


class API_Category(TypedDict):
    """
    Category type used in the Ed API.

    This is a non-recursive version of the cateogry type;
    subcategories are stored as strings.
    """

    name: str
    subcategories: list[str]
    thread_template: Optional[ContentString]


class API_Category_Recursive(TypedDict):
    """
    Category type used in the Ed API.

    This is a recursive version of the cateogry type;
    subcategories are also stored as API_Category_Recursive dicts.
    """

    name: str
    subcategories: list["API_Category_Recursive"]
    thread_template: Optional[ContentString]
