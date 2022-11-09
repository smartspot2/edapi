"""
Thread type used in the Ed API.
"""

from typing import Optional, TypedDict

from .content import ContentString
from .user import API_User_Short


class API_Thread(TypedDict):
    """
    Thread type used in the Ed API.
    """

    id: int  # global post number
    user_id: int  # user who created the post
    course_id: int
    editor_id: int
    accepted_id: Optional[int]
    duplicate_id: Optional[int]
    number: int  # post number relative to the course
    type: str
    title: str
    content: ContentString
    document: str  # rendered version of content
    category: str
    subcategory: str
    subsubcategory: str
    flag_count: int
    star_count: int
    view_count: int
    unique_view_count: int
    vote_count: int
    reply_count: int
    unresolved_count: int
    is_locked: bool
    is_pinned: bool
    is_private: bool
    is_endorsed: bool
    is_answered: bool
    is_student_answered: bool
    is_staff_answered: bool
    is_archived: bool
    is_anonymous: bool
    is_megathread: bool
    anonymous_comments: bool
    approved_status: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    pinned_at: Optional[str]
    anonymous_id: int
    vote: int
    is_seen: bool
    is_starred: bool
    is_watched: bool
    glanced_at: str
    new_reply_count: int
    duplicate_title: Optional[str]


class API_Thread_WithComments(API_Thread):
    """
    Thread type with comments and answers included.
    """

    answers: list["API_Thread_Comment"]
    comments: list["API_Thread_Comment"]


class API_Thread_WithUser(API_Thread):
    """
    Thread type with user information included.
    """

    user: API_User_Short


class API_Thread_Comment(TypedDict):
    """
    Comment type; included in the thread type with comments and answers.
    """

    id: int
    user_id: int
    course_id: int
    thread_id: int
    parent_id: Optional[int]
    editor_id: Optional[int]
    number: int
    type: str  # only seen comment
    kind: str  # only seen normal
    content: ContentString
    document: str  # rendered version of content
    flag_count: int
    vote_count: int
    is_endorsed: bool
    is_anonymous: bool
    is_private: bool
    is_resolved: bool
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]
    anonymous_id: int
    vote: int
    comments: list["API_Thread_Comment"]  # recursive for replies
