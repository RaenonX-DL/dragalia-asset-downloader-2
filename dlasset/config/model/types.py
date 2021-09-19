"""Type definitions for the config."""
from typing import Literal

__all__ = ("ExportType",)

# Should be the same as the listed enums in the config schema
# Names with `-` are the extended export type for special actions
ExportType = Literal[
    "MonoBehaviour",
    "GameObject",
    "AnimatorController",
    "AnimatorOverrideController",
    "Texture2D",
    "Texture2D-Alpha",
    "Sprite"
]
