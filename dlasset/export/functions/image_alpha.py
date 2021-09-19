"""Implementations to export image with alpha channel."""
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_alpha",)


def export_image_alpha(export_info_list: list["ExportInfo"]) -> None:
    """Export the image object with alpha channel merged into it according to ``export_info``."""
    for export_info in export_info_list:
        obj = export_info.obj

        export_path = os.path.join(export_info.export_dir, f"{obj.name}.png")

        img = obj.image
        img.save(export_path)
