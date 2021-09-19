"""Implementations to export image with alpha channel."""
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlasset.export import ExportInfoPathDict

__all__ = ("export_image_alpha",)


def export_image_alpha(info_path_dict: "ExportInfoPathDict") -> None:
    """Export the image objects in ``info_path_dict`` with alpha channel merged."""
    for export_info in info_path_dict.values():
        obj = export_info.obj

        export_path = os.path.join(export_info.export_dir, f"{obj.name}.png")

        img = obj.image
        img.save(export_path)
