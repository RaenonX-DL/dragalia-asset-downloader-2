"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import Optional, Sequence

from UnityPy.classes import MonoBehaviour, Object

from dlasset.config import AssetTaskFilter
from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

__all__ = ("select_mono_behaviour", "export_mono_behaviour",)


def select_mono_behaviour(objects: list[Object], filters: Optional[Sequence[AssetTaskFilter]] = None) -> list[Object]:
    """Get a list of asset ``MonoBehaviour`` objects to export."""
    objects_to_export: list[Object] = []

    for obj in objects:
        # DON'T use `!=` because this is using `__eq__` override for comparison
        # `__ne__` is not properly overridden
        if obj.type not in ("MonoBehaviour",):
            continue

        if filters and not any(filter_.match_container(obj.container) for filter_ in filters):
            continue

        objects_to_export.append(obj)

    return objects_to_export


def export_mono_behaviour(obj: MonoBehaviour, export_dir: str) -> Optional[MonoBehaviourTree]:
    """
    Export ``obj`` to ``export_dir``.

    Returns the mono behaviour type tree ``dict`` if exported.
    """
    export_dir_obj = os.path.join(export_dir, os.path.dirname(os.path.normpath(obj.container)))
    export_path: str = os.path.join(export_dir_obj, f"{obj.name}.json")

    if not obj.serialized_type.nodes:
        log("WARNING", f"No exportable node for {obj.name}")
        return None

    tree = obj.read_typetree()
    with open(export_path, "w+", encoding="utf-8") as f:
        f.write(json.dumps(tree, ensure_ascii=False, indent=2))

    return tree
