# TODO: Implement the lessons endpoint

from typing import Any, Optional, TypedDict
from ..user import API_User


# === GET /api/lessons/<lesson_id> ===
# also used by /api/courses/<course_id>/lessons/<lesson_number>?view=1

class API_GetLesson(TypedDict):
    """
    Response type for GET /api/lessons/<lesson_id>.

    Also used by GET /api/courses/<course_id>/lessons/<lesson_number>?view=1.
    """
    
    # Lesson fields. Not all fields are included.
    lesson: 53507 # temp class id
    id: int
    title: str
    type: str 
    kind: str 
    openable: bool # Whether the lesson is open or closed
    status: str 
    due_at: str # ISO 8601 date-time string
    created_at: str # ISO 8601 date-time string
