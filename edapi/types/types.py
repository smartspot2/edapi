"""
High level type classes used in the Ed API Integration.
"""

from typing import TypedDict


class EdError(RuntimeError):
    """
    Base exception for Ed API errors.
    """


class EdAuthError(EdError):
    """
    Raised when the API token is invalid.
    """


class EditThreadParams(TypedDict, total=False):
    """
    Parameters for editing an existing thread.
    Omit parameters to leave them untouched.
    """

    type: str
    title: str
    category: str
    subcategory: str
    subsubcategory: str
    content: str
    is_pinned: bool
    is_private: bool
    is_anonymous: bool
    is_megathread: bool
    anonymous_comments: bool


class PostThreadParams(TypedDict, total=True):
    """
    Parameters for posting a new thread.
    All parameters are required.
    """

    type: str
    title: str
    category: str
    subcategory: str
    subsubcategory: str
    content: str
    is_pinned: bool
    is_private: bool
    is_anonymous: bool
    is_megathread: bool
    anonymous_comments: bool
