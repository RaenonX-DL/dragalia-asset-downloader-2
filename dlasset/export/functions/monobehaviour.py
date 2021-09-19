"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import Any, Optional, Sequence

from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter
from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

__all__ = ("export_mono_behaviour",)


def export_mono_behaviour(
        asset: UnityAsset,
        export_dir: str,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[MonoBehaviourTree]:
    """
    Export ``MonoBehaviour`` objects as json in ``asset`` to ``export_dir``.

    Returns the exported mono behaviour trees.
    """
    trees: list[dict[Any, Any]] = []

    for obj in asset.objects:
        # DON'T use `!=` because this is using `__eq__` override for comparison
        # `__ne__` is not properly overridden
        if obj.type not in ("MonoBehaviour",):
            continue

        # Skip exporting the object that doesn't match any of the filter by container
        if filters and not any(filter_.match_container(obj.container) for filter_ in filters):
            continue

        # Only read-in the object after passing the container scan
        # - Object name is not available until read()
        # - Container name is available before read()
        # - Doing so speeds up the filtering process
        obj = obj.read()

        export_dir_obj = os.path.join(export_dir, os.path.dirname(os.path.normpath(obj.container)))
        export_path: str = os.path.join(export_dir_obj, f"{obj.name}.json")

        if not obj.serialized_type.nodes:
            log("WARNING", f"No exportable node for {obj.name}")
            return []

        tree = obj.read_typetree()
        with open(export_path, "w+", encoding="utf-8") as f:
            f.write(json.dumps(tree, ensure_ascii=False, indent=2))

        trees.append(tree)

    return trees
