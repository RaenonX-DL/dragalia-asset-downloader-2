"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import TYPE_CHECKING

from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfoPathDict

__all__ = ("export_image",)


def export_image(info_path_dict: "ExportInfoPathDict") -> None:
    """Export the image objects in ``info_path_dict``."""
    for export_info in info_path_dict.values():
        obj = export_info.obj

        log("INFO", f"Exporting {obj.name} ({export_info.container})...")

        export_path = os.path.join(export_info.export_dir, f"{obj.name}.png")

        img = obj.image
        img.save(export_path)
