"""Type definitions for the config."""
from typing import Literal

__all__ = ("UnityType", "ExportType")

# Should follow the naming of `UnityPy`
# List supported types only
UnityType = Literal[
    "MonoBehaviour",
    "MonoScript",
    "GameObject",
    "AnimatorController",
    "AnimatorOverrideController",
    "Texture2D",
    "Sprite",
    "Material"
]

# Special types that performs some special actions
# Names should be in the format of <UNITY_TYPE>-<NAME>.
ExtendedType = Literal[
    "Texture2D-Alpha",
    "Texture2D-Material",
    "Texture2D-Story",
    "Sprite-UI"
]

# Should be the same as the listed enums for the field `type`
ExportType = Literal[UnityType, ExtendedType]
