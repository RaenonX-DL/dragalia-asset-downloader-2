"""Implementations to export ``MonoBehaviour``."""
import json
import os
from typing import Optional, TYPE_CHECKING

from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_mono_behaviour",)


def export_mono_behaviour(export_info: "ExportInfo") -> Optional[MonoBehaviourTree]:
    """
    Export ``MonoBehaviour`` object according to ``export_info``.

    Returns the exported mono behaviour trees.
    """
    obj = export_info.obj

    export_path: str = os.path.join(export_info.export_dir, f"{obj.name}.json")

    if not obj.serialized_type.nodes:
        log("WARNING", f"No exportable data for {obj.name}")
        return None

    tree = obj.read_typetree()
    with open(export_path, "w+", encoding="utf-8") as f:
        f.write(json.dumps(tree, ensure_ascii=False, indent=2))

    return tree
