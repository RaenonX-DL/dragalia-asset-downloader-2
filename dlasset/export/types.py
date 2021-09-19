"""Type definitions for exporting the assets."""
from typing import Any, Callable, Literal, Union

from UnityPy.classes import MonoBehaviour

__all__ = ("ObjectType", "ExportFunction", "ExportReturn", "MonoBehaviourTree")

ObjectType = Literal["MonoBehaviour"]

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[[MonoBehaviour, str], MonoBehaviourTree]

ExportFunction = Union[
    MonoBehaviourExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
