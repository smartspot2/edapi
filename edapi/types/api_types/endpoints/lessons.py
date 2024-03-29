# TODO: Implement more specific types for the lesson endpoint

from typing import TypedDict
from ..user import API_User
from ..lesson import API_Lesson


# === GET /api/lessons/<lesson_id> ===
# also used by /api/courses/<course_id>/lessons/<lesson_number>?view=1

class API_GetLesson(TypedDict):
    """
    Response type for GET /api/lessons/<lesson_id>.

    Also used by GET /api/courses/<course_id>/lessons/<lesson_number>?view=1.
    """

    lesson: list[API_Lesson]

