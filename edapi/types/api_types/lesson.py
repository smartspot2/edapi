from typing import TypedDict, Optional

# Note: This should be all we need to define the Lesson type.

class API_Lesson(TypedDict):
    """
    Lesson type used in the Ed API.
    """

    # Lesson fields. Not all fields are included.
    id: int
    title: str
    type: str 
    kind: str 
    openable: bool # Whether the lesson is open or closed
    status: str 
    due_at: str # ISO 8601 date-time string
    created_at: str # ISO 8601 date-time string

    # Optional fields