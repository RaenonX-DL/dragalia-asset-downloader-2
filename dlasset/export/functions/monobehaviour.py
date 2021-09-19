"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import Optional

from UnityPy.classes import MonoBehaviour

from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

__all__ = ("export_mono_behaviour",)


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
