"""Implementations to export ``AnimatorController``."""
import os
from typing import TYPE_CHECKING

from dlasset.log import log
from dlasset.utils import export_json

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_anim_ctrl",)


def export_anim_ctrl(export_info: "ExportInfo") -> None:
    """Export ``AnimatorController`` objects in ``export_info``."""
    for obj_info in export_info.objects:
        obj = obj_info.obj

        log("INFO", f"Exporting AnimatorController: {obj.name} ({obj_info.container})")

        export_path: str = os.path.join(export_info.get_export_dir_of_obj(obj_info), f"{obj.name}.json")

        tree = obj.read_typetree()

        # TOS should be a `dict`
        tree["m_TOS"] = dict(tree["m_TOS"])

        clips = []
        for clip in tree["m_AnimationClips"]:
            clip_path_id = clip["m_PathID"]

            clip_obj = export_info.get_obj_info(clip_path_id, obj_info).obj

            clips.append({
                "$PathID": clip["m_PathID"],
                "$Name": clip_obj.name,
                "$StopTime": clip_obj.m_MuscleClip.m_StopTime
            })

        export = {"$Controller": tree, "$Clips": clips}

        export_json(export_path, export)
