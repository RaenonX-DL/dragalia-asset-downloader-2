"""Type definitions for exporting the assets."""
from typing import Any, Callable

from .model import ExportInfo
from .result import ExportResult

__all__ = ("ExportFunction", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

ExportFunction = Callable[[ExportInfo], ExportResult]
