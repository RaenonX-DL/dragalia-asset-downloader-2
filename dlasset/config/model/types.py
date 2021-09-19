"""Type definitions for the config."""
from typing import Literal

__all__ = ("ObjectType",)

# This should be the same the listed enums in the config schema
ObjectType = Literal[
    "MonoBehaviour",
    "GameObject",
    "AnimatorController",
    "AnimatorOverrideController",
    "Texture2D",
    "Sprite"
]
