"""Implementations to export image with alpha channel."""
import os
from typing import Optional, TYPE_CHECKING, cast

from PIL import Image
from UnityPy.classes import Texture2D

from dlasset.enums import WarningType
from dlasset.export.result import ExportResult
from dlasset.log import log
from dlasset.model import ObjectInfo
from .image import export_image

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_alpha",)


def get_alpha_channel_tex(texture_envs: dict, export_info: "ExportInfo", material: ObjectInfo) -> Optional[Texture2D]:
    """Get the alpha texture. Returns ``None`` if not available."""
    if "_AlphaTex" not in texture_envs:  # Alpha channel texture not available
        return None

    path_id_alpha = texture_envs["_AlphaTex"]["m_Texture"]["m_PathID"]

    if not path_id_alpha:  # Path ID points to null (path ID = 0)
        return None

    return cast(Texture2D, export_info.get_obj_info(path_id_alpha, material).obj)


def export_image_alpha(export_info: "ExportInfo") -> ExportResult:
    """Export the image objects in ``export_info`` with alpha channel merged."""
    material = next((info for info in export_info.objects if info.obj.type == "Material"), None)

    if not material:
        if WarningType.NO_MATERIAL not in export_info.suppressed_warnings:
            log("WARNING", f"Asset {export_info} does not have any `Material` - fallback to normal image export")
        return export_image(export_info)

    log("DEBUG", f"Reading material data... ({material.container})")

    tree = material.obj.read_typetree()

    texture_envs = dict(tree["m_SavedProperties"]["m_TexEnvs"])

    path_id_main = texture_envs["_MainTex"]["m_Texture"]["m_PathID"]

    if not path_id_main:  # Main texture points to null file - don't return anything
        return ExportResult()

    info_main = export_info.get_obj_info(path_id_main, material)
    obj_main = info_main.obj

    log("INFO", f"Exporting image with alpha merge of {obj_main.name}... ({info_main.container})")

    export_path = os.path.join(export_info.get_export_dir_of_obj(info_main), f"{obj_main.name}.png")

    log("DEBUG", f"Merging alpha channel of {obj_main.name}... ({info_main.container})")

    img_main = obj_main.image
    if obj_alpha := get_alpha_channel_tex(texture_envs, export_info, material):
        # Alpha texture exists, merge image
        img_alpha = obj_alpha.image

        # Alpha texture could be in a different size
        if img_alpha.size != img_main.size:
            img_alpha = img_alpha.resize(img_main.size)

        r, g, b = img_main.split()[:3]
        a = img_alpha.split()[3]

        Image.merge("RGBA", (r, g, b, a)).save(export_path)
        return ExportResult(exported_paths=[export_path])

    # Alpha texture does not exist, just save it
    img_main.save(export_path)
    return ExportResult(exported_paths=[export_path])
