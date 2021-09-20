"""Implementations to export image with alpha channel."""
import os
from typing import Optional, TYPE_CHECKING, cast

from PIL import Image
from UnityPy.classes import Texture2D

from dlasset.log import log
from .image import export_image

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_alpha",)


def get_alpha_channel_tex(texture_envs: dict, export_info: "ExportInfo") -> Optional[Texture2D]:
    """Get the alpha texture. Returns ``None`` if not available."""
    if "_AlphaTex" not in texture_envs:  # Alpha channel texture not available
        return None

    path_id_alpha = texture_envs["_AlphaTex"]["m_Texture"]["m_PathID"]

    if not path_id_alpha:  # Path ID points to null (path ID = 0)
        return None

    return cast(Texture2D, export_info.get_obj_info(path_id_alpha).obj)


def export_image_alpha(export_info: "ExportInfo") -> None:
    """Export the image objects in ``export_info`` with alpha channel merged."""
    material = next((info for info in export_info.objects if info.obj.type == "Material"), None)

    if not material:
        log("INFO", f"Asset {export_info} does not have any `Material` - fallback to normal image export")
        export_image(export_info)
        return

    log("DEBUG", f"Reading material data... ({material.container})")

    tree = material.obj.read_typetree()

    texture_envs = dict(tree["m_SavedProperties"]["m_TexEnvs"])

    path_id_main = texture_envs["_MainTex"]["m_Texture"]["m_PathID"]

    if not path_id_main:  # Main texture points to null file - don't return anything
        return

    info_main = export_info.get_obj_info(path_id_main)
    obj_main = info_main.obj

    log("INFO", f"Exporting image with alpha merge of {obj_main.name}... ({info_main.container})")

    export_path = os.path.join(export_info.get_export_dir_of_obj(info_main), f"{obj_main.name}.png")

    log("DEBUG", f"Merging alpha channel of {obj_main.name}... ({info_main.container})")

    if obj_alpha := get_alpha_channel_tex(texture_envs, export_info):
        # Alpha texture exists, merge image
        img_main = obj_main.image
        img_alpha = obj_alpha.image

        # Alpha texture could be in a different size
        if img_alpha.size != img_main.size:
            img_alpha = img_alpha.resize(img_main.size)

        r, g, b = img_main.split()[:3]
        a = img_alpha.split()[3]

        Image.merge("RGBA", (r, g, b, a)).save(export_path)
        return

    # Alpha texture does not exist, just save it
    obj_main.image.save(export_path)
