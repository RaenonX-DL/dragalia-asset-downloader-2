"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import TYPE_CHECKING

from dlasset.log import log

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image",)


def export_image(export_info_list: list["ExportInfo"]) -> None:
    """Export the image object according to ``export_info``."""
    for export_info in export_info_list:
        obj = export_info.obj

        log("INFO", f"Exporting {obj.name} ({export_info.container})...")

        export_path = os.path.join(export_info.export_dir, f"{obj.name}.png")

        img = obj.image
        img.save(export_path)
