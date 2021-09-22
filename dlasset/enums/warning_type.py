"""Enum for the types of warning."""
from enum import Enum

__all__ = ("WarningType",)


class WarningType(Enum):
    """
    Types of warning message.

    Values should be the same as the listed enums for the field ``suppressWarnings``.
    """

    NOTHING_TO_EXPORT = "nothingToExport"
    NO_MAIN_TEXTURE = "noMainTexture"
    NO_PARTS_INFO = "noPartsInfo"
    NO_MATERIAL = "noMaterial"
