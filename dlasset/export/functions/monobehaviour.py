"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import TYPE_CHECKING

from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_mono_behaviour",)


def export_mono_behaviour(export_info: "ExportInfo") -> list[MonoBehaviourTree]:
    """
    Export ``MonoBehaviour`` objects in ``export_info``.

    Returns the exported mono behaviour trees.
    """
    trees: list[MonoBehaviourTree] = []

    for obj_info in export_info.objects:
        obj = obj_info.obj

        log("INFO", f"Exporting {obj.name} ({obj_info.container})...")

        export_path: str = os.path.join(export_info.get_export_dir_of_obj(obj_info), f"{obj.name}.json")

        if not obj.serialized_type.nodes:
            log("WARNING", f"No exportable data for {obj.name}")
            continue

        tree = obj.read_typetree()
        with open(export_path, "w+", encoding="utf-8") as f:
            f.write(json.dumps(tree, ensure_ascii=False, indent=2))

        trees.append(tree)

    return trees
