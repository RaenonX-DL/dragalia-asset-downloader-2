"""Type definitions for exporting the assets."""
from typing import Any, Callable, Union

from .model import ExportInfo

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[[list[ExportInfo]], list[MonoBehaviourTree]]

Texture2DExportFunction = Callable[[list[ExportInfo]], None]

ExportFunction = Union[
    MonoBehaviourExportFunction,
    Texture2DExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
