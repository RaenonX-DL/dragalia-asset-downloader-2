"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Union

from .model import ExportInfo

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[[ExportInfo], Optional[MonoBehaviourTree]]

Texture2DExportFunction = Callable[[ExportInfo], None]

ExportFunction = Union[
    MonoBehaviourExportFunction,
    Texture2DExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
