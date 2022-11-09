# edapi Documentation

As the Ed API is still in beta, any of the official endpoints can change, and is mainly for personal reference as I'm working through the creation of the API.

## Authorization

### `EdAPI.api_token`

Stored API token from the `.env` file.

This API token is also stored as a header in the `requests.Session` object for authentication, used for all requests with the Ed API.

### `EdAPI.login()`

Prompt user to fetch and register an API token with a `.env` file.

If the token is found, then a brief validation check through `EdAPI.get_user_info()` is done; if this call returns `None`, then the authorization failed; otherwise, the authorizaton succeeded, and the user info is stored in an instance variable.

## API Interface

- `EdAPI.get_user_info()`

  Retrieves the user info.

- `EdAPI.list_user_activity(user_id, course_id, limit: int = 30, offset: int = 0, filter: str = "all")`

  Retrieves a list of comments and thread made by the user.

  - `limit`: maximum number of entries to retrieve (default: 30, clipped to 50)

  - `offset`: offset for pagination in retrieving user activity (default 0)

  - `filter`: filter for what user activity to retrieve (default: "all")

    Possible filters include: "all", "thread", "answer", "comment"

- `EdAPI.list_threads(course_id: int, limit: int = 30, offset: int = 0, sort: str = "new")`

  Retrieves a list of threads associated with the course.

  - `limit`: maximum number of threads to retrieve (default: 30, clipped to 100)

  - `offset`: offset for pagination in retrieving threads

  - `sort`: how to sort the threads (default: `"new"`)

  Returns a list of [`Thread`](#thread) dicts.

- `EdAPI.get_thread(thread_id: int)`

  Retrieve the details for a thread, given its id.

  Returns a [`Thread`](#thread) dict.

- `EdAPI.get_course_thread(course_id: int, thread_number: int)`

  Retrieve the details for a thread in a course, given the course id and the thread number.

  This is usually more suitable from the user's standpoint, as the website UI displays thread with respect to their course thread number, not the global thread id.

  Returns a [`Thread`](#thread) dict.

- `EdAPI.edit_thread(thread_id: int, params: EditThreadParams)`

  Edits the given thread.

  The `params` dict is of the following format; any of the following can be omitted to make it unchanged.

  ```python
  {
    "type": ThreadType,
    "title": str,
    "category": str,
    "subcategory": str,
    "subsubcategory": str,
    "content": str,
    "is_pinned": bool,
    "is_private": bool,
    "is_anonymous": bool,
    "is_megathread": bool,
    "anonymous_comments": bool,
  }
  ```

  Returns the API response JSON dict.

- `EdAPI.post_thread(course_id: int, params: PostThreadParams)`

  Creates a new thread.

  See `edit_thread` for the `params` dict; the only difference here is that all values are required when creating a new thread.

  Returns the API response JSON dict.

- `EdAPI.upload_file(filename: str, file: bytes, content_type: str)`

  Uploads a file to Ed.

  Parameters:

  - `filename`: Name of file to upload; associated with the `FormData` when uploading.
  - `file`: Raw file bytes, straight from Python's `open(filename, "rb")`.
  - `content_type`: Content type (MIME type) of the file.
    - For PNG images, this is `image/png`; for ZIP files, this is `multipart/form-data`, etc.

  Returns the link to the uploaded file.

## Document Format

I'll be referring to a string containing a document throughout the following documentation as a `ContentString` type, for ease of reference.

### Tags

The below tags are the common tags used in the bodies of Ed posts; the structure is in XML, so BeautifulSoup can be used to programmatically create these documents.

- `<document version="2.0">`: Document tag, always surrounding everything
- `<heading level="">`: Heading text
  - `level`: heading level; 1 is the largest heading text size.
- `<paragraph>`: Normal text
  - All text must be in a paragraph tag.
- `<bold>`: Bold text
- `<italic>`: Italic text
- `<underline>`: Underlined text
- `<math>`: LaTeX text
- `<link href="">`: Link
  - `href`: Link URL
- `<list style="">`: List
  - `style`: One of `bullet` (unordered) or `number` (ordered)
- `<list-item>`: List item
  - Must be inside a `<list>` tag.
  - Text items must be surrounded with a `<paragraph>` tag within the list item.
- `<callout type="type">`: Callout bubble
  - `type`: One of `success`, `info`, `warning`, or `error`
- `<code>`: Inline code block (no syntax highlighting)
- `<pre>`: Code block (no syntax highlighting)
  - There is no need to surround this with the `<paragraph>` tag.
- `<snippet language="language" runnable="boolean">`: Code snippet (with syntax highlighting)
  - `language`: Syntax highlighting language
  - `runnable`: Whether the code snippet should be runnable
- `<spoiler>`: Spoiler text
  - There is no need to surround this with the `<paragraph>` tag.
  - Spoiler text must be surrounded in a `<paragraph>` tag.
- `<figure>`: Container for images
- `<image src="" width="" height="">`: Embed image
  - `src`: image URL
  - `width`, `height`: image width and height; the image is automatically scaled to fit the window, but this defines the aspect ratio.
- `<file url="">`: Embed file

## Reverse-engineering the API

The following are some notes while working through the exposed API endpoints that the actual website uses while interacting with the site. The API is still in beta, so these are subject to change; it's mostly for personal reference that I have them documented here.

### Recurring structures

#### Course

Lots of the values here are unknown, and likely not useful for our purposes here.

```python
{
  "id": int,
  "realm_id": int,
  "code": str,
  "name": str,
  "year": str,
  "session": str,
  "status": str,  # "archived" or "active"
  "features": {
    "analytics": bool,
    "resources": bool,
    "discussion": bool,
    "messages": bool,
    "chat": bool,
    "challenges": bool,
    "challenge_services": bool,
    "intermediate_files": bool,
    "git_submission": bool,
    "workspaces": bool,
    "leaderboard": bool,
    "assessments": bool,
    "lessons": bool,
    "sway": bool,
    "exams": bool,
    "bots": bool,
    "bots_v2": bool
  },
  "settings": {
    "default_page": str,
    "user_lab_enrollment": bool,
    "lab_user_agent_regex": str,
    "lockdown_user_agent_regex": str,
    "access_codes_enabled": bool,
    "setup_status": str,
    "discussion": {
      "private": bool,
      "private_threads_only": bool,
      "anonymous_comments": bool,
      "anonymous_comments_override": bool,
      "anonymous": bool,
      "anonymous_to_staff": bool,
      "threads_require_approval": bool,
      "unread_indicator_hidden": bool,
      "deleted": bool,
      "categories": Category[],  # non-recursive version
      "categories_new": Category[],  # recursive version
      "thread_templates_enabled": bool,
      "category_unselected": bool,
      "snippet_languages": str[],
      "default_snippet_language": str,
      "rejection_comment_template": ContentString | null,
      "bot_source": null,  # unknown what these options are for
      "bot_enabled": bool,
      "bot_enabled_v2": bool,
      "full_announcement_emails": bool,
      "no_digests": bool,
      "digest_interval": null,
      "saved_replies_enabled": bool,
      "saved_replies": [
        {
          "name": str,
          "content": ContentString
        }, ...
      ],
      "sortable_feed": bool,
      "default_feed_sort": str,
      "thread_numbers": bool,
      "comment_numbers": bool,
      "tutorial_badge_visible_to_all": bool,
      "readonly": bool,
      "show_all_pinned_threads": bool,
      "comment_endorsements": bool
    },
    "chat": {
      "student_dm_student": bool,
      "student_dm_staff": bool,
      "channels_enabled": bool
    },
    "lesson": {
      "quiz_question_auto_submit": bool,
      "merged_quiz_settings_enabled": bool,
      "merged_challenge_settings_enabled": bool,
      "scheduling_enabled": bool,
      "karel_slide_enabled": bool,
      "workspace_partition_slide_enabled": bool,
      "autoplay_videos": bool
    },
    "workspace": {
      "preset": null,
      "internet": null,
      "lizardfs": null,
      "inactivity_timeout": null,
      "default_type": "",
      "student_creation_disabled": bool,
      "remote_desktop": bool,
      "remote_app": bool,
      "saturn_override": bool,
      "saturn_default_kernel": "",
      "disable_student_workspace_upload": bool,
      "env": null,
      "settings": {
        "rstudio_layout": ""
      }
    },
    "challenge_workspace": {
      "preset": null,
      "internet": null,
      "lizardfs": null,
      "inactivity_timeout": null,
      "default_type": "",
      "student_creation_disabled": bool,
      "remote_desktop": bool,
      "remote_app": bool,
      "saturn_override": bool,
      "saturn_default_kernel": "",
      "disable_student_workspace_upload": bool,
      "env": null,
      "settings": {
        "rstudio_layout": ""
      }
    },
    "code_editor": {
      "show_invisibles": null,
      "detect_indentation": null,
      "soft_tabs": null,
      "tab_size": null,
      "autocomplete": null
    },
    "theme": {
      "logo": str,
      "background": str,
      "foreground": str
    },
    "role_labels": {
      "student": str,
      "mentor": str,
      "tutor": str,
      "staff": str,
      "admin": str
    },
    "soft_tabs": null,
    "tab_size": null,
    "voiceover": bool,
    "highlightable_languages": str[],
    "user_avatars_enabled": bool,
    "snippet_language_override": str | null,
    "codecast_enabled": bool,
    "codecast_student_creation_disabled": bool,
    "poll_enabled": bool,
    "poll_student_creation_disabled": bool,
    "scratch_enabled": bool,
    "hide_emails_from_staff": bool,
    "queue_marking": bool,
    "queue_parallelism": int,
    "queue_limit": int
  },
  "created_at": str,
  "is_lab_regex_active": bool
}
```

#### Category

There seems to be two different kinds of category structures; `categories` and `new_categories`.

With the normal `categories`, it seems like the `subcategories` key only has a list of strings for the names of subcategories:

```python
{
  "name": str,
  "subcategories": str[],
  "thread_template": ContentString | null
}
```

With the `new_categories` (perhaps to replace the current `categories`), the `subcategories` key is fully recursive:

```python
{
  "name": str,
  "subcategories": Category[],
  "thread_template": ContentString | null
}
```

#### Thread

```python
{
  "id": int,  # global post number
  "user_id": int,  # user who created the post
  "course_id": int,
  "editor_id": int,
  "accepted_id": int | null,
  "duplicate_id": int | null,
  "number": int,  # post number relative to the course
  "type": str,
  "title": str,
  "content": ContentString,
  "document": str,  # rendered version of content
  "category": str,
  "subcategory": str,
  "subsubcategory": str,
  "flag_count": int,
  "star_count": int,
  "view_count": int,
  "unique_view_count": int,
  "vote_count": int,
  "reply_count": int,
  "unresolved_count": int,
  "is_locked": bool,
  "is_pinned": bool,
  "is_private": bool,
  "is_endorsed": bool,
  "is_answered": bool,
  "is_student_answered": bool,
  "is_staff_answered": bool,
  "is_archived": bool,
  "is_anonymous": bool,
  "is_megathread": bool,
  "anonymous_comments": bool,
  "approved_status": str,
  "created_at": str,
  "updated_at": str,
  "deleted_at": str | null,
  "pinned_at": str | null,
  "anonymous_id": int,
  "vote": int,
  "is_seen": bool,
  "is_starred": bool,
  "is_watched": bool,
  "glanced_at": str,
  "new_reply_count": int,
  "duplicate_title": str | null,
  "answers": Comment[],  # always type "answer"
  "comments": Comment[]  # always type "comment"
}
```

#### Comment

Associated with the [`Thread`](#thread) datatype.

```python
{
  "id": int,
  "user_id": int,
  "course_id": int,
  "thread_id": int,
  "parent_id": int | null,
  "editor_id": int | null,
  "number": int,
  "type": str,  # "comment" or "answer"
  "kind": str,  # only seen "normal"
  "content": ContentString,
  "document": str,  # rendered version of content
  "flag_count": int,
  "vote_count": int,
  "is_endorsed": bool,
  "is_anonymous": bool,
  "is_private": bool,
  "is_resolved": bool,
  "created_at": str,
  "updated_at": str | null,
  "deleted_at": str | null,
  "anonymous_id": int,
  "vote": int,
  "comments": Comment[]  # recursive for replies
}
```

### Endpoints

#### `GET /api/user`

Fetch user details, along with details for all associated courses and associated realms.

Response:

```python
{
  "courses": [
    {
      "course": Course,
      "role": {
      "user_id": int,
      "course_id": int,
      "lab_id": int | null,
      "role": str,
      "tutorial": null,  # unsure what this is for
      "digest": bool,
      "settings": {
      "digest_interval": int | null,  # interval in minutes
      "email_announcements": bool | null
      },
      "created_at": str,
      "deleted_at": str | null
      },
      "lab": null  # unsure what this is for
    }, ...
  ],
  "realms": [
    {
      "id": int,
      "name": str,
      "type": str,
      "domain": str,
      "features": {},  # unsure what these are
      "settings": {
        "course_inactive_on_lti_creation": bool,
        "allow_course_creation": bool,
        "lti_and_course_creation": bool,
        "force_framebuster": bool,
        "lti_compact": bool,
        "discuss_shared_category": str,
        "theme": {
          "logo": str,
          "accent_color": str
        },
        "sourced_id_as_unique_identifier": bool,
        "lms_user_id_as_sourced_id": bool,
        "default_page_discussion": bool,
        "no_student_role_upgrade": bool,
        "segregated": bool,
        "can_disable_discussion": bool,
        "allow_anonymous_comments": bool,
        "allow_comment_numbers": bool,
        "force_name_update": bool
      },
      "role": str
    }, ...
  ],
  "time": str,
    "user": {
      "id": int,
      "role": str,
      "name": str,
      "email": str,
      "username": str | null,
      "avatar": str | null,
      "features": {},  # unsure what these are
      "settings": {
      "digest_interval": int | null,
      "discuss_feed_style": str,
      "accessible": bool,
      "locale": str,
      "theme": str,  # "light" or "dark"
      "character_key_shortcuts_disabled": bool,
      "set_tz_automatically": bool,
      "tz": str,  # timezone
      "reply_via_email": bool,
      "email_announcements": bool,
      "email_watched_threads": bool,
      "email_thread_replies": bool,
      "email_comment_replies": bool,
      "email_mentions": bool,
      "mention_direct_message_digest_interval": str,
      "channel_digest_interval": str,
      "allow_password_login": bool,
      "desktop_notifications_enabled": bool,
      "desktop_notifications_scope": str,
      "snooze_end": str
    },
    "activated": bool,
    "created_at": str,
    "course_role": str | null,
    "secondary_emails": str[],
    "has_password": bool,
    "is_lti": bool,
    "is_sso": bool,
    "can_change_name": bool,
    "has_pats": bool,
    "realm_id": int | null
  }
}
```

#### `GET /api/threads/<thread_id>`

Fetches details for a given thread, along with all users involved in the thread.

Response:

```python
{
  "thread": Thread,
  "users": [  # list of users involved in the thread
    {
      "avatar": str,
      "course_role": str,
      "id": int,
      "name": str,
      "role": str
    }, ...
  ]
}
```

#### `GET /api/courses/<course_id>/threads/<thread_number>`

Fetches details for a given thread, relative to a given course.

The `thread_number` in the URL is not the thread id, but rather the number assigned within the course.

Response: See `GET /api/threads/<thread_id>`.

#### `POST /api/courses/<course_id>/threads`

Creates a new thread in a given course.

Request:

```python
{
    "thread": {
        "type": "post",
        "title": "Test",
        "category": "General",
        "subcategory": "",
        "subsubcategory": "",
        "content": "<document version=\"2.0\"><paragraph>Test</paragraph></document>",
        "is_pinned": false,
        "is_private": true,
        "is_anonymous": false,
        "is_megathread": false,
        "anonymous_comments": false
    }
}
```

Response:

```python
{
  "bot": {  # details on bot execution
    "validation": {
      "execution": {
        "type": str,
        "cpu_time": int,
        "wall_time": int,
        "heap_size": int,
        "origin": str,
        "line": int,
        "column_start": int,
        "column_end": int,
        "stack_trace": str
      },
      "warnings": [],
      "errors": []
    },
    "pre": {
      "execution": {
        "type": str,
        "cpu_time": int,
        "wall_time": int,
        "heap_size": int,
        "origin": str,
        "line": int,
        "column_start": int,
        "column_end": int,
        "stack_trace": str
      },
      "thread": {
        "user": {
          "name": str,
          "role": str,
          "tutorial": int | null
        },
        "type": str,
        "title": str,
        "category": str,
        "subcategory": str,
        "subsubcategory": str,
        "send_emails": bool,
        "xml": str,
        "plaintext": str,
        "is_private": bool,
        "is_anonymous": bool,
        "is_pinned": bool,
        "is_megathread": bool
      },
      "actions": []
    },
    "post": {
        "execution": {
            "type": str,
            "cpu_time": int,
            "wall_time": int,
            "heap_size": int,
            "origin": str,
            "line": int,
            "column_start": int,
            "column_end": int,
            "stack_trace": str
        },
        "thread": {
            "user": {
                "name": str,
                "role": str,
                "tutorial": int | null
            },
            "type": str,
            "title": str,
            "category": str,
            "subcategory": str,
            "subsubcategory": str,
            "send_emails": bool,
            "xml": str,
            "plaintext": str,
            "is_private": bool,
            "is_anonymous": bool,
            "is_pinned": bool,
            "is_megathread": bool
        },
        "actions": []
    }
  },
  "status": str,
  "thread": Thread
}
```

#### `PUT /api/threads/<thread_id>`

Edits an existing thread.

Request:

```python
{
  "thread": {  # subset of Thread fields
    "type": str,
    "title": str,
    "category": str,
    "subcategory": str,
    "subsubcategory": str,
    "content": ContentString,
    "is_pinned": bool,
    "is_private": bool,
    "is_anonymous": bool,
    "is_megathread": bool,
    "anonymous_comments": bool
  }
}
```

Response:

```python
{
  "status": str,  # "ok"
  "thread": {  # subset of Thread fields
    "id": int,
    "user_id": int,
    "course_id": int,
    "editor_id": int,
    "accepted_id": int | null,
    "duplicate_id": int | null,
    "number": int,
    "type": str,
    "title": str,
    "content": ContentString,
    "document": str,
    "category": str,
    "subcategory": str,
    "subsubcategory": str,
    "flag_count": int,
    "star_count": int,
    "view_count": int,
    "unique_view_count": int,
    "vote_count": int,
    "reply_count": int,
    "unresolved_count": int,
    "is_locked": bool,
    "is_pinned": bool,
    "is_private": bool,
    "is_endorsed": bool,
    "is_answered": bool,
    "is_student_answered": bool,
    "is_staff_answered": bool,
    "is_archived": bool,
    "is_anonymous": bool,
    "is_megathread": bool,
    "anonymous_comments": bool,
    "approved_status": str,  # "approved"
    "created_at": str,
    "updated_at": str,
    "deleted_at": str | null,
    "pinned_at": str | null,
    "anonymous_id": int
  }
}
```

#### `POST /api/files`

Uploads a file to Ed.

The resulting file can be accessed at `https://static.us.edusercontent.com/files/<id>` (region can differ).

Request: `FormData` object containing the file with key `attachment`.

Response:

```python
{
  "file": {
    "user_id": int,
    "id": str,
    "filename": str,
    "extension": str,
    "created_at": str
  }
}
```

#### `POST /api/files/url`

Uploads a file to Ed, from a given URL.

The resulting file can be accessed at `https://static.us.edusercontent.com/files/<id>` (region can differ).

Request:

```python
{
  "url": str
}
```

Response: See `POST /api/files`.

#### `POST /api/threads/<thread_id>/pin`

Pins the given thread.

#### `POST /api/threads/<thread_id>/unpin`

Unpins the given thread.

#### `POST /api/threads/<thread_id>/endorse`

Endorses the given thread.

#### `POST /api/threads/<thread_id>/unendorse`

Unendorses the given thread.

#### `POST /api/threads/<thread_id>/lock`

Locks the given thread.

#### `POST /api/threads/<thread_id>/unlock`

Unlocks the given thread.

#### `POST /api/threads/<thread_id>/star`

Stars the given thread.

#### `POST /api/threads/<thread_id>/unstar`

Unstars the given thread.

#### `GET /api/users/<user_id>/profile/activity`

Retrieves a list of all activity for a given user.

```python
{
  "items": [
    {
      "type": "comment",
      "value": {
        "id": int,
        "type": "comment" | "answer",
        "document": str,
        "course_id": int,
        "course_name": str,
        "course_code": str,
        "thread_id": int,
        "thread_title": str,
        "thread_category": str,
        "thread_subcategory": str,
        "thread_subsubcategory": str,
        "created_at": str,
      }
    },
    # OR
    {
      "type": "thread",
      "value": {
        "id": int,
        "type": "post" | "question" | "announcement",
        "course_id": int,
        "course_name": str,
        "course_code": str,
        "title": str,
        "document": str,
        "category": str,
        "subcategory": str,
        "subsubcategory": str,
        "is_private": bool,
        "approved_status": str,
        "created_at": str
      }
    }
  ]
}
```
