"""Enums for asset locale."""
from enum import Enum

__all__ = ("Locale",)


class Locale(Enum):
    """Asset locale enum."""

    CHT = "tw"
    CHS = "cn"
    EN = "en"
    JP = "jp"
