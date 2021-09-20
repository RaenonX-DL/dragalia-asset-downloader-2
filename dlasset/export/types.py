"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Union

from .model import ExportInfo

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

ExportReturn = Union[
    list[MonoBehaviourTree],
    None
]

ExportFunction = Callable[[ExportInfo], Optional[list[MonoBehaviourTree]]]
