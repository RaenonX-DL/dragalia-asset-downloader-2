"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image",)


def export_image(export_info: "ExportInfo") -> None:
    """Export the image object according to ``export_info``."""
    obj = export_info.obj

    export_path = os.path.join(export_info.export_dir, f"{obj.name}.png")

    img = obj.image
    img.save(export_path)
