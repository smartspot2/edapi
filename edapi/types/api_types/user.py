"""
User type used in the Ed API.

There are two kinds of user types; the full type with all fields,
and a shortened type with only a subset of the fields.
"""

from typing import Any, Optional, TypedDict


class API_User(TypedDict):
    """
    Full user type.
    """

    id: int
    role: str
    name: str
    email: str
    username: Optional[str]
    avatar: Optional[str]
    features: Any  # unsure what these are
    settings: "API_User_Settings"
    activated: bool
    created_at: str
    course_role: Optional[str]
    secondary_emails: list[str]
    has_password: bool
    is_lti: bool
    is_sso: bool
    can_change_name: bool
    has_pats: bool
    realm_id: Optional[int]


class API_User_Short(TypedDict):
    """
    Abbreviated user type.
    """

    avatar: str
    course_role: str
    id: int
    name: str
    role: str
    tutorials: dict[int, str]


class API_User_WithEmail(TypedDict):
    """
    User type with email; returned by the analytics endpoint.
    """

    avatar: Optional[str]
    course_role: Optional[str]
    email: str
    name: str
    user_id: int
    username: Optional[str]


class API_User_Settings(TypedDict):
    """
    User settings type, included in the full user type.
    """

    digest_interval: Optional[int]
    discuss_feed_style: str
    accessible: bool
    locale: str
    theme: str  # light or dark
    character_key_shortcuts_disabled: bool
    set_tz_automatically: bool
    tz: str  # timezone
    reply_via_email: bool
    email_announcements: bool
    email_watched_threads: bool
    email_thread_replies: bool
    email_comment_replies: bool
    email_mentions: bool
    mention_direct_message_digest_interval: str
    channel_digest_interval: str
    allow_password_login: bool
    desktop_notifications_enabled: bool
    desktop_notifications_scope: str
    snooze_end: str
