"""Utility functions for handling HTTP requests."""
from requests import Response, Session
from requests.adapters import HTTPAdapter

__all__ = ("http_get",)


def http_get(url: str) -> Response:
    """Get the content on ``url``."""
    session = Session()
    session.mount(url, HTTPAdapter(max_retries=5))
    return session.get(url)
