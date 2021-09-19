"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import TYPE_CHECKING

from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfoPathDict

__all__ = ("export_mono_behaviour",)


def export_mono_behaviour(info_path_dict: "ExportInfoPathDict") -> list[MonoBehaviourTree]:
    """
    Export ``MonoBehaviour`` objects in ``ExportInfoPathDict``.

    Returns the exported mono behaviour trees.
    """
    trees: list[MonoBehaviourTree] = []

    for export_info in info_path_dict.values():
        obj = export_info.obj

        log("INFO", f"Exporting {obj.name} ({export_info.container})...")

        export_path: str = os.path.join(export_info.export_dir, f"{obj.name}.json")

        if not obj.serialized_type.nodes:
            log("WARNING", f"No exportable data for {obj.name}")
            continue

        tree = obj.read_typetree()
        with open(export_path, "w+", encoding="utf-8") as f:
            f.write(json.dumps(tree, ensure_ascii=False, indent=2))

        trees.append(tree)

    return trees
