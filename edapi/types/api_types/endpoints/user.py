"""
Types for /api/user endpoint.
"""

from typing import Any, Optional, TypedDict

from ..course import API_Course
from ..user import API_User


class API_User_Response(TypedDict):
    """
    Response type for GET /api/user.
    """

    courses: list["API_User_Response_Course"]
    realms: list["API_User_Response_Realm"]
    time: str
    user: API_User


class API_User_Response_Course(TypedDict):
    """
    Course type included in the user info response.
    """

    course: API_Course
    role: "API_User_Response_Course_Role"  # user role in the course
    lab: None  # unsure what this is for


class API_User_Response_Course_Role(TypedDict):
    """
    Course role type included in the user info response.
    """

    user_id: int
    course_id: int
    lab_id: Optional[int]
    role: str
    tutorial: None  # unsure what this is for
    digest: bool
    settings: "API_User_Response_Course_Role_Settings"
    created_at: str
    deleted_at: Optional[str]


class API_User_Response_Course_Role_Settings(TypedDict):
    """
    Course role settings type included in the user info response.
    """

    digest_interval: Optional[int]  # interval in minutes
    email_announcements: Optional[bool]


class API_User_Response_Realm(TypedDict):
    """
    Realm type included in the user info response.

    Usually represents a school/organization.
    """

    id: int
    name: str
    type: str
    domain: str
    features: Any  # unsure what these are
    settings: "API_User_Response_Realm_Settings"
    role: str


class API_User_Response_Realm_Settings(TypedDict):
    """
    Realm settings type included in the user info response.
    """

    course_inactive_on_lti_creation: bool
    allow_course_creation: bool
    lti_and_course_creation: bool
    force_framebuster: bool
    lti_compact: bool
    discuss_shared_category: str
    theme: "API_User_Response_Realm_Settings_Theme"
    sourced_id_as_unique_identifier: bool
    lms_user_id_as_sourced_id: bool
    default_page_discussion: bool
    no_student_role_upgrade: bool
    segregated: bool
    can_disable_discussion: bool
    allow_anonymous_comments: bool
    allow_comment_numbers: bool
    force_name_update: bool


class API_User_Response_Realm_Settings_Theme(TypedDict):
    """
    Realm settings theme type included in the user info response.
    """

    logo: str
    accent_color: str
