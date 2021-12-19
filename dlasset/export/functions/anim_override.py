"""Implementations to export ``AnimatorOverrideController``."""
import os
from typing import TYPE_CHECKING

from dlasset.export.result import ExportResult
from dlasset.log import log
from dlasset.utils import export_json

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_anim_override",)


def export_anim_override(export_info: "ExportInfo") -> ExportResult:
    """Export ``AnimatorController`` objects in ``export_info``."""
    export_paths = []

    for obj_info in export_info.objects:
        obj = obj_info.obj

        log("INFO", f"Exporting AnimatorOverrideController: {obj.name} ({obj_info.container})")

        export_path: str = os.path.join(export_info.get_export_dir_of_obj(obj_info), f"{obj.name}.json")

        tree = obj.read_typetree()

        clips = []
        for clip in tree["m_Clips"]:
            clip_override_pptr = clip["m_OverrideClip"]
            clip_ov_path_id = clip_override_pptr["m_PathID"]

            # No override, no need to write the info
            if not clip_ov_path_id:
                continue

            clip_ov = export_info.get_obj_info(clip_ov_path_id, obj_info).obj

            clips.append({
                "$Name": clip_ov.name,
                "$OriginalClip": clip["m_OriginalClip"],
                "$OverrideClip": clip_override_pptr,
                "$StopTime": clip_ov.m_MuscleClip.m_StopTime,
            })

        export = {"$Name": obj.name, "$Clips": clips}

        export_json(export_path, export)

        export_paths.append(export_path)

    return ExportResult(exported_paths=export_paths)
