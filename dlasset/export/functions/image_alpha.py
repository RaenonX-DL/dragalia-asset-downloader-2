"""Implementations to export image with alpha channel."""
import os
from typing import TYPE_CHECKING

from PIL import Image

from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfoPathDict

__all__ = ("export_image_alpha",)


def export_image_alpha(info_path_dict: "ExportInfoPathDict") -> None:
    """Export the image objects in ``info_path_dict`` with alpha channel merged."""
    material = next(info for info in info_path_dict.values() if info.obj.type == "Material")

    log("DEBUG", f"Reading material data... ({material.container})")

    tree = material.obj.read_typetree()

    texture_envs = dict(tree["m_SavedProperties"]["m_TexEnvs"])

    path_id_alpha = texture_envs["_AlphaTex"]["m_Texture"]["m_PathID"]
    path_id_main = texture_envs["_MainTex"]["m_Texture"]["m_PathID"]

    info_main = info_path_dict[path_id_main]

    obj_alpha = info_path_dict[path_id_alpha].obj
    obj_main = info_main.obj

    export_dir = info_main.export_dir

    log("INFO", f"Exporting {obj_main.name}... ({info_main.container})")

    export_path = os.path.join(export_dir, f"{obj_main.name}.png")

    log("DEBUG", f"Merging alpha channel of {obj_main.name}... ({info_main.container})")

    r, g, b = obj_main.image.split()[:3]
    a = obj_alpha.image.split()[3]

    Image.merge("RGBA", (r, g, b, a)).save(export_path)
