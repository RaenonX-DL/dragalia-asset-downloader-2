"""Implementations to export ``Sprite`` from UI."""
from typing import TYPE_CHECKING

from dlasset.log import log
from dlasset.model import ObjectInfo
from .image import export_image_of_obj

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_sprite_ui",)


def export_sprites_from_mono_behaviour(export_info: "ExportInfo", mono_info: ObjectInfo) -> None:
    """Export ``Sprite``s from the ``MonoBehaviour`` object in ``mono_info``."""
    log("DEBUG", f"Reading sprites data in mono behaviour... ({mono_info.container})")

    sprite_path_ids = [pptr["m_PathID"] for pptr in mono_info.obj.read_typetree()["sprites"]]

    if not sprite_path_ids:
        log("WARNING", f"No exportable sprites for {mono_info.container}")
        return

    for sprite_path_id in sprite_path_ids:
        sprite_obj_info = export_info.get_obj_info(sprite_path_id, mono_info)
        export_image_of_obj(export_info, sprite_obj_info)


def export_sprite_ui(export_info: "ExportInfo") -> None:
    """Export ``Sprite`` according to ``export_info`` for UI."""
    for obj_info in export_info.objects:
        obj_type = obj_info.obj.type

        if obj_type == "MonoBehaviour":
            export_sprites_from_mono_behaviour(export_info, obj_info)
        elif obj_type == "Sprite":
            export_image_of_obj(export_info, obj_info)
        else:
            raise ValueError(f"Unknown object type for UI sprite export: {obj_type}")
