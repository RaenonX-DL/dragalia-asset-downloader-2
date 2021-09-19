"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Sequence, Union

from UnityPy.classes import MonoBehaviour, Object
from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter

__all__ = ("SelectFunction", "ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

SelectFunction = Callable[[UnityAsset, Optional[Sequence[AssetTaskFilter]]], list[Object]]

MonoBehaviourExportFunction = Callable[[MonoBehaviour, str], Optional[MonoBehaviourTree]]

ExportFunction = Union[
    MonoBehaviourExportFunction
]

ExportReturn = Union[
    MonoBehaviourTree
]
