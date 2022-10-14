"""
Types for endpoints involving creating and updating threads.
"""

from typing import Any, Optional, TypedDict

from ..content import ContentString
from ..thread import API_Thread_WithComments, API_Thread_WithUser
from ..user import API_User_Short

# === GET /api/threads/<thread_id> ===
# also used by /api/courses/<course_id>/threads/<thread_number>


class API_GetThread_Response(TypedDict):
    """
    Response type for GET /api/threads/<thread_id>.

    Also used by GET /api/courses/<course_id>/threads/<thread_number>.
    """

    thread: API_Thread_WithComments
    users: list[API_User_Short]  # list of users involved in the thread


# === GET /api/courses/<course_id>/threads ===


class API_ListThreads_Response(TypedDict):
    """
    Response type for GET /api/courses/<course_id>/threads.
    """

    sort_key: str
    threads: list[API_Thread_WithUser]
    users: list[API_User_Short]  # list of users involved in the threads


# === POST /api/courses/<course_id>/threads ===


class API_PostThread_Request(TypedDict):
    """
    Request type for POST /api/courses/<course_id>/threads.
    """

    thread: "API_PostThread_Request_Thread"


class API_PostThread_Request_Thread(TypedDict):
    """
    Thread type used in the request for POST /api/courses/<course_id>/threads.
    """

    type: str
    title: str
    category: str
    subcategory: str
    subsubcategory: str
    content: ContentString
    is_pinned: bool
    is_private: bool
    is_anonymous: bool
    is_megathread: bool
    anonymous_comments: bool


class API_PostThread_Response(TypedDict):
    """
    Response type for POST /api/courses/<course_id>/threads.
    """

    bot: Any  # TODO: inplement bot types
    status: str  # only seen "ok"
    thread: API_Thread_WithUser


# === PUT /api/threads/<thread_id> ===


class API_PutThread_Request(TypedDict):
    """
    Request type for PUT /api/threads/<thread_id>.
    """

    thread: "API_PutThread_Request_Thread"


class API_PutThread_Request_Thread(API_PostThread_Request_Thread, total=False):
    """
    Thread type used in the request for PUT /api/courses/<course_id>/threads.

    Exactly the same as the POST request, but with optional fields.
    """


class API_PutThread_Response(TypedDict):
    """
    Response type for PUT /api/threads/<thread_id>.
    """

    status: str  # only seen "ok"
    thread: "API_PutThread_Response_Thread"


class API_PutThread_Response_Thread(TypedDict):
    """
    Thread type included in the response for PUT /api/threads/<thread_id>.

    The thread object returned from a PUT request is very weird;
    it doesn't have any of the ["vote, "is_seen", "is_starred",
    "is_watched", "glanced_at", "new_reply_count", "duplicate_title"]
    fields.

    The present fields are copied from API_Thread.
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
