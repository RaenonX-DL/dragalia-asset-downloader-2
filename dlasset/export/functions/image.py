"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import TYPE_CHECKING

from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image",)


def export_image(export_info: "ExportInfo") -> None:
    """Export the image objects in ``info_path_dict``."""
    for obj_info in export_info.objects:
        obj = obj_info.obj

        log("INFO", f"Exporting image of {obj.name} ({obj_info.container})...")

        export_path = os.path.join(export_info.get_export_dir_of_obj(obj_info), f"{obj.name}.png")

        img = obj.image
        img.save(export_path)
