"""Implementations to export image with alpha channel."""
import os
from typing import TYPE_CHECKING

from PIL import Image

from dlasset.log import log
from .image import export_image

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_alpha",)


def export_image_alpha(export_info: "ExportInfo") -> None:
    """Export the image objects in ``export_info`` with alpha channel merged."""
    material = next((info for info in export_info.objects if info.obj.type == "Material"), None)

    if not material:
        log("INFO", f"Asset {export_info.asset_name} does not have any `Material` - fallback to normal image export")
        export_image(export_info)
        return

    log("DEBUG", f"Reading material data... ({material.container})")

    tree = material.obj.read_typetree()

    texture_envs = dict(tree["m_SavedProperties"]["m_TexEnvs"])

    path_id_alpha = texture_envs["_AlphaTex"]["m_Texture"]["m_PathID"]
    path_id_main = texture_envs["_MainTex"]["m_Texture"]["m_PathID"]

    info_main = export_info.get_obj_info(path_id_main)
    obj_main = info_main.obj

    log("INFO", f"Exporting {obj_main.name}... ({info_main.container})")

    export_path = os.path.join(export_info.get_export_dir_of_obj(info_main), f"{obj_main.name}.png")

    log("DEBUG", f"Merging alpha channel of {obj_main.name}... ({info_main.container})")

    obj_alpha = export_info.get_obj_info(path_id_alpha).obj if path_id_alpha else None
    if obj_alpha:
        # Alpha texture exists, merge image
        r, g, b = obj_main.image.split()[:3]
        a = obj_alpha.image.split()[3]
        Image.merge("RGBA", (r, g, b, a)).save(export_path)
    else:
        # Alpha texture does not exist, just save it
        obj_main.image.save(export_path)
