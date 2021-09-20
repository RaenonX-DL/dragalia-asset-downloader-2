"""Enums for asset locale."""
from enum import Enum

__all__ = ("Locale",)


class Locale(Enum):
    """Asset locale enum."""

    CHT = "tw"
    CHS = "cn"
    EN = "en"
    JP = "jp"

    @property
    def is_master(self) -> bool:
        """Check if the locale is the master locale (JP)."""
        return self == Locale.JP
