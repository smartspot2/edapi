"""
Types for endpoints involving retrieving resources.
"""

from typing import Any, Optional, TypedDict

from ..resources import API_Resource

# === GET /api/resources/<resource_id> ===

class API_GetResource_Response(TypedDict):
    """
    Response type for GET /api/resources/<resource_id>.
    """

    resources: API_Resource