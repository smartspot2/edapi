from typing import List, Optional, TypedDict

from ..user import API_User_WithEmail


class API_Analytics_Users_Response(TypedDict):
    """
    Response type for GET /api/courses/<course_id>/analytics/users.
    """

    users: List[API_User_WithEmail]


class API_Analytics_Enrollments_Response(TypedDict):
    """
    Response type for GET /api/courses/<course_id>/analytics/enrollments.

    Enrollment data from the course analytics.
    """

    enrolled_users: int
    total_students: int
    total_users: int
