"""
ContentString type used in the Ed API.

This is merely a string, but the type is used to differentiate between
other arbitrary strings.
"""


class ContentString(str):
    """
    Wrapper for a string that represents an XML document content,
    used for thread bodies.
    """
