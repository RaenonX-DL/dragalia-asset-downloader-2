"""Implementations to export image according to the ``Material`` of the same asset."""
from typing import TYPE_CHECKING

from .image_story import export_image_story

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_material",)


def export_image_material(export_info: "ExportInfo") -> None:
    """Export the images in ``export_info`` with YCbCr channel merged."""
    export_image_story(export_info, crop_parts_base=False)
