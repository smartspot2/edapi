"""
Activity type used in the Ed API.
"""

from typing import Literal, TypedDict, Union


class API_ListUserActivity_Response(TypedDict):
    """
    Response type for GET /api/users/<user_id>/profile/activity
    """

    items: list["API_ListUserActivity_Response_Item"]


# Union type for both comment and thread items
API_ListUserActivity_Response_Item = Union[
    "API_ListUserActivity_Response_CommentItem",
    "API_ListUserActivity_Response_ThreadItem",
]


class API_ListUserActivity_Response_CommentItem(TypedDict):
    """
    Item type for a comment, included in the user activity response
    """

    type: Literal["comment"]
    value: "API_ListUserActivity_Response_CommentItem_Value"


class API_ListUserActivity_Response_ThreadItem(TypedDict):
    """
    Item type for a thread, included in the user activity response
    """

    type: Literal["thread"]
    value: "API_ListUserActivity_Response_ThreadItem_Value"


class API_ListUserActivity_Response_CommentItem_Value(TypedDict):
    id: int
    type: str
    course_code: str
    course_id: int
    course_name: str
    created_at: str
    document: str
    thread_id: int
    thread_title: str
    thread_category: str
    thread_subcategory: str
    thread_subsubcategory: str


class API_ListUserActivity_Response_ThreadItem_Value(TypedDict):
    id: int
    type: str
    approved_status: str
    course_code: str
    course_id: int
    course_name: str
    document: str
    title: str
    category: str
    subcategory: str
    subsubcategory: str
    is_private: bool
    created_at: str
