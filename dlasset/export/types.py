"""Type definitions for exporting the assets."""
from typing import Any, Callable, Optional, Sequence, Union

from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter

__all__ = ("ExportFunction", "ExportReturn", "MonoBehaviourTree")

MonoBehaviourTree = dict[Any, Any]

MonoBehaviourExportFunction = Callable[
    [UnityAsset, str, Optional[Sequence[AssetTaskFilter]]],
    list[MonoBehaviourTree]
]

ExportFunction = Union[
    MonoBehaviourExportFunction
]

ExportReturn = Union[
    list[MonoBehaviourTree]
]
