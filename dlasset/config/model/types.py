"""Type definitions for the config."""
from typing import Literal, Union

__all__ = ("UnityType", "ExportType",)

# Should follow the naming of `UnityPy`
# List supported types only
UnityType = Literal[
    "MonoBehaviour",
    "GameObject",
    "AnimatorController",
    "AnimatorOverrideController",
    "Texture2D",
    "Sprite"
]

# Should be the same as the listed enums in the config schema
# Names with `-` are the extended export type for special actions
ExportType = Union[
    UnityType,
    Literal[
        "Texture2D-Alpha"
    ],
]
