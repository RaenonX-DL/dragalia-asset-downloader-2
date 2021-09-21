"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import TYPE_CHECKING

from dlasset.log import log
from dlasset.model import ObjectInfo

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image", "export_image_of_obj")


def export_image_of_obj(export_info: "ExportInfo", obj_info: ObjectInfo) -> None:
    """Export the image in ``obj_info``."""
    obj = obj_info.obj

    log("INFO", f"Exporting image of {obj.name} ({obj_info.container})...")

    export_path = os.path.join(export_info.get_export_dir_of_obj(obj_info), f"{obj.name}.png")

    img = obj.image
    img.save(export_path)


def export_image(export_info: "ExportInfo") -> None:
    """Export the image objects in ``export_info``."""
    for obj_info in export_info.objects:
        export_image_of_obj(export_info, obj_info)
