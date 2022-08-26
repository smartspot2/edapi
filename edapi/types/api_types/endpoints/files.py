"""
Types for endpoints involving files.
"""

from typing import TypedDict

# === POST /api/files ===
# No request type here, as the request body is a formdata object.


class API_PostFile_Response(TypedDict):
    """
    Response type for POST /api/files.
    """

    file: "API_PostFile_Response_File"


class API_PostFile_Response_File(TypedDict):
    """
    File type used in the response for POST /api/files.
    """

    user_id: int
    id: str
    filename: str
    extension: str
    created_at: str


# === POST /api/files/url ===
# Response type is the same as the /api/files endpoint.


class API_PostFileUrl_Request(TypedDict):
    """
    Request type for POST /api/files/url.
    """

    url: str
