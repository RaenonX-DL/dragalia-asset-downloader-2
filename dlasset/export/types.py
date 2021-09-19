"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Union

from UnityPy.classes import MonoBehaviour

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[[MonoBehaviour, str], Optional[MonoBehaviourTree]]

ExportFunction = Union[
    MonoBehaviourExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
