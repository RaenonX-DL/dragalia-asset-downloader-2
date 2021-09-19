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

Texture2DExportFunction = Callable[
    [UnityAsset, str, Optional[Sequence[AssetTaskFilter]]],
    None
]

ExportFunction = Union[
    MonoBehaviourExportFunction,
    Texture2DExportFunction
]

ExportReturn = Union[
    list[MonoBehaviourTree],
    None
]
