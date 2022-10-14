"""
Course type used in the Ed API.
"""

from typing import Optional, TypedDict

from .category import API_Category, API_Category_Recursive
from .content import ContentString


class API_Course(TypedDict):
    """
    Course type used in the Ed API.
    """

    id: int
    realm_id: int
    code: str
    name: str
    year: str
    session: str
    status: str  # archived or active
    features: "API_Course_Features"
    settings: "API_Course_Settings"
    created_at: str
    is_lab_regex_active: bool


class API_Course_Features(TypedDict):
    """
    Course features type included in the course type.
    """

    analytics: bool
    resources: bool
    discussion: bool
    messages: bool
    chat: bool
    challenges: bool
    challenge_services: bool
    intermediate_files: bool
    git_submission: bool
    workspaces: bool
    leaderboard: bool
    assessments: bool
    lessons: bool
    sway: bool
    exams: bool
    bots: bool
    bots_v2: bool
    admin: str


class API_Course_Settings(TypedDict):
    """
    Course settings type included in the course type.
    """

    default_page: str
    user_lab_enrollment: bool
    lab_user_agent_regex: str
    lockdown_user_agent_regex: str
    access_codes_enabled: bool
    setup_status: str
    discussion: "API_Course_Settings_Discussion"
    chat: "API_Course_Settings_Chat"
    lesson: "API_Course_Settings_Lesson"
    workspace: "API_Course_Settings_Workspace"
    challenge_workspace: "API_Course_Settings_Workspace"
    code_editor: "API_Course_Settings_CodeEditor"
    theme: "API_Course_Settings_Theme"
    role_labels: "API_Course_Settings_RoleLabels"
    soft_tabs: None
    tab_size: None
    voiceover: bool
    highlightable_languages: list[str]
    user_avatars_enabled: bool
    snippet_language_override: Optional[str]
    codecast_enabled: bool
    codecast_student_creation_disabled: bool
    poll_enabled: bool
    poll_student_creation_disabled: bool
    scratch_enabled: bool
    hide_emails_from_staff: bool
    queue_marking: bool
    queue_parallelism: int
    queue_limit: int


class API_Course_Settings_Discussion(TypedDict):
    """
    Course discussion settings type included in the course settings type.
    """

    private: bool
    private_threads_only: bool
    anonymous_comments: bool
    anonymous_comments_override: bool
    anonymous: bool
    anonymous_to_staff: bool
    threads_require_approval: bool
    unread_indicator_hidden: bool
    deleted: bool
    categories: list[API_Category]  # non-recursive version
    categories_new: list[API_Category_Recursive]  # recursive version
    thread_templates_enabled: bool
    category_unselected: bool
    snippet_languages: list[str]
    default_snippet_language: str
    rejection_comment_template: Optional[ContentString]
    bot_source: None  # unknown what these options are for
    bot_enabled: bool
    bot_enabled_v2: bool
    full_announcement_emails: bool
    no_digests: bool
    digest_interval: None
    saved_replies_enabled: bool
    saved_replies: list["API_Course_Settings_Discussion_SavedReply"]
    sortable_feed: bool
    default_feed_sort: str
    thread_numbers: bool
    comment_numbers: bool
    tutorial_badge_visible_to_all: bool
    readonly: bool
    show_all_pinned_threads: bool
    comment_endorsements: bool


class API_Course_Settings_Discussion_SavedReply(TypedDict):
    """
    Course discussion saved reply type included in the discussion settings type.
    """

    name: str
    content: ContentString


class API_Course_Settings_Chat(TypedDict):
    """
    Course chat settings type included in the course settings type.
    """

    student_dm_student: bool
    student_dm_staff: bool
    channels_enabled: bool


class API_Course_Settings_Lesson(TypedDict):
    """
    Course lesson settings type included in the course settings type.
    """

    quiz_question_auto_submit: bool
    merged_quiz_settings_enabled: bool
    merged_challenge_settings_enabled: bool
    scheduling_enabled: bool
    karel_slide_enabled: bool
    workspace_partition_slide_enabled: bool
    autoplay_videos: bool


class API_Course_Settings_Workspace(TypedDict):
    """
    Course workspace settings type included in the course settings type.
    """

    preset: None
    internet: None
    lizardfs: None
    inactivity_timeout: None
    default_type: str
    student_creation_disabled: bool
    remote_desktop: bool
    remote_app: bool
    saturn_override: bool
    saturn_default_kernel: str
    disable_student_workspace_upload: bool
    env: None
    settings: "API_Course_Settings_Workspace_Settings"


class API_Course_Settings_Workspace_Settings(TypedDict):
    """
    Course workspace settings type included in the course workspace settings type.
    """

    rstudio_layout: str


class API_Course_Settings_CodeEditor(TypedDict):
    """
    Course code editor settings type included in the course settings type.
    """

    show_invisibles: None
    detect_indentation: None
    soft_tabs: None
    tab_size: None
    autocomplete: None


class API_Course_Settings_Theme(TypedDict):
    """
    Course theme settings type included in the course settings type.
    """

    logo: str
    background: str
    foreground: str


class API_Course_Settings_RoleLabels(TypedDict):
    """
    Course role labels type included in the course settings type.
    """

    student: str
    mentor: str
    tutor: str
    staff: str
