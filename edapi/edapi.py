"""
Module for interacting with the Ed API.
"""

import json
import os
from typing import NoReturn, Optional

import requests
from dotenv import find_dotenv, load_dotenv
from requests.compat import urljoin

from .types import EdAuthError, EdError, EditThreadParams, PostThreadParams
from .types.api_types.endpoints.activity import (
    API_ListUserActivity_Response,
    API_ListUserActivity_Response_Item,
)
from .types.api_types.endpoints.files import API_PostFile_Response
from .types.api_types.endpoints.threads import (
    API_GetThread_Response,
    API_ListThreads_Response,
    API_PostThread_Response,
    API_PutThread_Request,
    API_PutThread_Response,
    API_PutThread_Response_Thread,
)
from .types.api_types.endpoints.user import API_User_Response
from .types.api_types.thread import API_Thread_WithComments, API_Thread_WithUser

ANSI_BLUE = lambda text: f"\u001b[34m{text}\u001b[0m"
ANSI_GREEN = lambda text: f"\u001b[32m{text}\u001b[0m"
ANSI_RED = lambda text: f"\u001b[31m{text}\u001b[0m"

API_BASE_URL = "https://us.edstem.org/api/"
STATIC_FILE_BASE_URL = "https://static.us.edusercontent.com/files/"

API_TOKEN_ENV_VAR = "ED_API_TOKEN"

AUTH_MESSAGE = f"""
Go to
    {ANSI_BLUE("https://edstem.org/us/settings/api-tokens")}
and create a new API token.

Create a {ANSI_BLUE(".env")} file (or set up environment variables) with the {API_TOKEN_ENV_VAR} environment variable set to the API token you just created.
"""


def _ensure_login(func):
    """
    Decorator to ensure the user is logged in before calling the function.
    """

    def login_wrapper(self, *args, **kwargs):
        if self.api_token is None:
            self.login()
        return func(self, *args, **kwargs)

    return login_wrapper


def _throw_error(message: str, error_content: bytes) -> NoReturn:
    """
    Throw an error with the given message and the error content.
    """
    error_json = json.loads(error_content)
    if error_json.get("code") == "bad_token":
        # auth error
        raise EdAuthError(
            {"message": f"Ed authentication error; {message}", "response": error_json}
        )

    # other error
    raise EdError({"message": message, "response": error_json})


class EdAPI:
    """
    Class for Ed API integration.

    This class is responsible for authenticating the user, and for making API calls to the Ed API.
    """

    def __init__(self):
        self.api_token = None
        self.session = requests.Session()

        self._load_api_token()

    def _load_api_token(self) -> Optional[API_User_Response]:
        """
        Read the API token from .env file; defaults to None if not found.

        Utilizes the `/api/user` endpoint to verify the token;
        returns the response if successful.
        """
        load_dotenv(find_dotenv(usecwd=True))
        self.api_token = os.getenv(API_TOKEN_ENV_VAR, None)
        if self.api_token is None:
            # unable to load API token
            return None

        # save session header as well
        self.session.headers.update(self._auth_header)

        # authorization check
        try:
            return self.get_user_info()
        except EdAuthError:
            # invalid api token; don't keep it
            self.api_token = None
            self._remove_auth_header()

        return None

    def login(self):
        """
        Log in to the Ed API with the API token.

        Continuously prompts for the API token if it is not found in the .env file.
        """
        user_info = None
        while self.api_token is None:
            print(AUTH_MESSAGE)
            input(ANSI_RED("Press ENTER when you have done so."))
            print()  # new line to divide next output
            user_info = self._load_api_token()

            if self.api_token is None:
                print(
                    ANSI_RED("Invalid API Token; make sure you have the correct token.")
                )

        if user_info is None:
            # only way this is reached is if the token was initially loaded successfully.
            user_info = self.get_user_info()

        # print login welcome message
        user_dict = user_info["user"]
        user_name = user_dict["name"]
        user_email = user_dict["email"]
        print(
            "Authentication successful;",
            f"logged in as {ANSI_GREEN(user_name)} ({ANSI_BLUE(user_email)})",
        )

    @property
    def _auth_header(self):
        """
        Auth header with the API token for all requests.
        """
        return {"Authorization": f"Bearer {self.api_token}"}

    def _remove_auth_header(self):
        """
        Remove the auth header from the session.
        """
        del self.session.headers["Authorization"]

    @_ensure_login
    def get_user_info(self) -> API_User_Response:
        """
        Retrieve the user info from Ed.
        """
        user_info_url = urljoin(API_BASE_URL, "user")
        response = self.session.get(user_info_url)
        if response.ok:
            return response.json()

        _throw_error("Failed to get user info.", response.content)

    @_ensure_login
    def list_user_activity(
        self,
        /,
        user_id: int,
        course_id: int,
        *,
        limit: int = 30,
        offset: int = 0,
        filter: str = "all",
    ) -> list[API_ListUserActivity_Response_Item]:
        """
        Retrieve a list of comments and threads made by the user.

        Limit can range from 1 to 50 (anything higher will get clipped to 50).
        Offset can be used to list out all activity for a user iteratively,
        through pagination.

        GET /api/users/<user_id>/profile/activity?courseID=<course_id>
        """
        list_url = urljoin(API_BASE_URL, f"users/{user_id}/profile/activity")
        response = self.session.get(
            list_url,
            params={
                "courseID": course_id,
                "limit": limit,
                "offset": offset,
                "filter": filter,
            },
        )
        if response.ok:
            response_json: API_ListUserActivity_Response = response.json()
            return response_json.get("items", [])  # default to empty list

        _throw_error(
            f"Failed to list user activity for user {user_id} in course {course_id}.",
            response.content,
        )

    @_ensure_login
    def list_threads(
        self, /, course_id: int, *, limit: int = 30, offset: int = 0, sort: str = "new"
    ) -> list[API_Thread_WithUser]:
        """
        Retrieve list of threads, with the given limit, offset, and sort.

        Limit can range from 1 to 100 (anything higher will get clipped to 100).
        Offset can be used to list out all of the threads in a course iteratively,
        through pagination.

        GET /api/courses/<course_id>/threads
        """
        list_url = urljoin(API_BASE_URL, f"courses/{course_id}/threads")
        response = self.session.get(
            list_url, params={"limit": limit, "offset": offset, "sort": sort}
        )
        if response.ok:
            response_json: API_ListThreads_Response = response.json()
            return response_json["threads"]

        _throw_error(
            f"Failed to list threads for course {course_id}.", response.content
        )

    @_ensure_login
    def get_thread(self, thread_id: int) -> API_Thread_WithComments:
        """
        Retrieve the details for a thread, given its id.

        GET /api/threads/<thread_id>
        """
        thread_url = urljoin(API_BASE_URL, f"threads/{thread_id}")
        response = self.session.get(thread_url)
        if response.ok:
            response_json: API_GetThread_Response = response.json()
            return response_json["thread"]

        _throw_error(f"Failed to get thread {thread_id}.", response.content)

    @_ensure_login
    def get_course_thread(
        self, course_id: int, thread_number: int
    ) -> API_Thread_WithComments:
        """
        Retrieve the details for a thread in a given course, using the thread number.

        GET /api/courses/<course_id>/threads/<thread_id>
        """
        thread_url = urljoin(
            API_BASE_URL, f"courses/{course_id}/threads/{thread_number}"
        )
        response = self.session.get(thread_url)
        if response.ok:
            response_json: API_GetThread_Response = response.json()
            return response_json["thread"]

        _throw_error(f"Failed to get thread {thread_number}.", response.content)

    @_ensure_login
    def post_thread(
        self, course_id: int, params: PostThreadParams
    ) -> API_Thread_WithUser:
        """
        Creates a new thread in the given course.

        POST /api/courses/<course_id>/threads

        Returns newly created thread object.
        """
        thread_url = urljoin(API_BASE_URL, f"courses/{course_id}/threads")
        response = self.session.post(thread_url, json={"thread": params})
        if response.ok:
            response_json: API_PostThread_Response = response.json()
            return response_json["thread"]

        _throw_error(f"Failed to post thread in course {course_id}.", response.content)

    @_ensure_login
    def edit_thread(
        self, thread_id: int, params: EditThreadParams
    ) -> API_PutThread_Response_Thread:
        """
        Edit the details for a given thread.

        PUT /api/threads/<thread_id>

        Returns newly created thread object.
        """

        thread = self.get_thread(thread_id)

        # set items
        for key, val in params.items():
            # ensure we're only modifying values that have appeared in the existing thread objectf
            if key in thread and val is not None:
                thread[key] = val

        thread_url = urljoin(API_BASE_URL, f"threads/{thread_id}")
        request_json: API_PutThread_Request = {"thread": thread}
        response = self.session.put(thread_url, json=request_json)
        if response.ok:
            response_json: API_PutThread_Response = response.json()
            return response_json["thread"]

        _throw_error(f"Failed to edit thread {thread_id}.", response.content)

    @_ensure_login
    def upload_file(self, filename: str, file: bytes, content_type: str) -> str:
        """
        Upload a file to Ed.

        `filename` is used as the filename for the file when uploading.
        `file` is the raw bytestream from `open(..., "rb")` after calling `.read()`.
        `content_type` is the MIME type of the file.

        POST /api/files

        Returns the static URL for the uploaded file.
        """
        upload_url = urljoin(API_BASE_URL, "files")
        # send file through formdata
        formdata = {"attachment": (filename, file, content_type)}
        response = self.session.post(upload_url, files=formdata)
        if response.ok:
            response_json: API_PostFile_Response = response.json()
            file_id = response_json["file"]["id"]
            return urljoin(STATIC_FILE_BASE_URL, file_id)

        _throw_error(f"Failed to upload file {filename}.", response.content)
