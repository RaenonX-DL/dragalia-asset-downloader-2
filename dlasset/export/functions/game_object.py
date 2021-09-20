"""Implementations to export ``GameObject`` and its component into a single script."""
import os
from typing import TYPE_CHECKING

from dlasset.export.types import MonoBehaviourTree
from dlasset.log import log
from dlasset.model import ObjectInfo
from dlasset.utils import export_json

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_game_object",)


def export_single_game_obj(export_info: "ExportInfo", game_obj_info: ObjectInfo) -> None:
    """Export a single game object."""
    tree_export: MonoBehaviourTree = {}

    object_tree = game_obj_info.obj.read_typetree()

    components = [
        export_info.get_obj_info(component["component"]["m_PathID"]).obj
        for component in object_tree["m_Component"][1:]  # 1st component is always a `Transform` which is omitted
    ]

    tree_name = object_tree["m_Name"]
    tree_components = []
    for component in components:
        component_tree = component.read_typetree()

        script_path_id = component_tree["m_Script"]["m_PathID"]
        if script_path_id:
            # Attach script type name if available
            attachment = {
                "$Script": export_info.get_obj_info(component_tree["m_Script"]["m_PathID"]).obj.name
            }
        else:
            # Otherwise, attach component name
            attachment = {"$Name": component_tree["m_Name"]}

        tree_components.append(attachment | component_tree)

    tree_export["Name"] = tree_name
    tree_export["Components"] = tree_components

    export_path: str = os.path.join(export_info.get_export_dir_of_obj(game_obj_info), f"{tree_name}.prefab.json")

    export_json(export_path, tree_export)


def export_game_object(export_info: "ExportInfo") -> None:
    """Export components in ``export_info`` info a single script for each game object."""
    game_obj_info_list = [obj_info for obj_info in export_info.objects if obj_info.obj.type == "GameObject"]

    if not game_obj_info_list:
        log("WARNING", f"No exportable `GameObject` from {export_info}")
        return

    for idx, game_obj_info in enumerate(game_obj_info_list):
        export_single_game_obj(export_info, game_obj_info)

        if idx % 50 == 0:
            log(
                "INFO",
                f"{idx} / {len(game_obj_info_list)} ({idx / len(game_obj_info_list):.2%}) objects exported "
                f"- {export_info}"
            )
