"""Type definitions for exporting the assets."""
from typing import Any, Callable, Union

from .model import ExportInfo

__all__ = ("ExportInfoPathDict", "ExportFunction", "ExportReturn", "MonoBehaviourTree")

ExportInfoPathDict = dict[int, ExportInfo]

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[[ExportInfoPathDict], list[MonoBehaviourTree]]

Texture2DExportFunction = Callable[[ExportInfoPathDict], None]

ExportFunction = Union[
    MonoBehaviourExportFunction,
    Texture2DExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
