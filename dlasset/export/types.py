"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Union

from .model import ExportInfo

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

ExportFunction = Callable[[ExportInfo], Optional[list[MonoBehaviourTree]]]

ExportReturn = Union[
    MonoBehaviourTree
]
