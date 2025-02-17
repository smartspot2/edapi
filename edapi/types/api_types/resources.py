"""
Resource type used in the Ed API.
"""

from typing import Optional, TypedDict

from .content import ContentString
from .user import API_User_Short


class API_Resource(TypedDict):
    """
    Resource type used in the Ed API.
    """

    id: int # resource id
    course_id: int 
    name: str # resource name
    session: str
    category: str # resource category 
    extension: str
    link: str
    size: int
    staff_only: bool
    embedding: bool
    release_at: Optional[str]
    created_at: str
    updated_at: Optional[str]