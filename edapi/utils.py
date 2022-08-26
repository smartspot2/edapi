"""
Various utility functions for the Ed API.
"""

from bs4 import BeautifulSoup, Tag


def new_document() -> tuple[BeautifulSoup, Tag]:
    """
    Creates a new BeautifulSoup instance for a new document.

    Returns the tuple (soup, root), where `soup` is the BeautifulSoup instance,
    and `root` is the root tag.
    """
    soup = BeautifulSoup('<document version="2.0"></document>', "xml")
    assert soup.document is not None  # type coercion
    return (soup, soup.document)


def parse_content(content: str) -> tuple[BeautifulSoup, Tag]:
    """
    Parses the content and returns a BeautifulSoup instance.

    Returns the tuple (soup, root), where `soup` is the BeautifulSoup instance,
    and `root` is the root tag.
    """
    soup = BeautifulSoup(content, "xml")
    assert soup.document is not None  # type coercion
    return (soup, soup.document)
