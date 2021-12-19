"""Implementations to export story emotion image."""
import os
from typing import TYPE_CHECKING, cast

from PIL import Image
from UnityPy.classes import Material

from dlasset.enums import WarningType
from dlasset.export.result import ExportResult
from dlasset.log import log
from dlasset.model import ObjectInfo
from dlasset.utils import crop_image, merge_y_cb_cr_a

if TYPE_CHECKING:
    from dlasset.export import ExportInfo

__all__ = ("export_image_story",)

# Almost same across all the assets
_parts_image_size = (256, 256)


def get_y_cb_cr_a_from_material(
        material: Material, export_info: "ExportInfo", root_mono_behaviour: ObjectInfo
) -> tuple[Image, Image, Image, Image]:
    """Get a tuple containing Y, Cb, Cr, alpha image object in order of the material."""
    texture_envs = dict(material.read_typetree()["m_SavedProperties"]["m_TexEnvs"])

    obj_y = export_info.get_obj_info(texture_envs["_TexY"]["m_Texture"]["m_PathID"], root_mono_behaviour).obj.image
    obj_cb = export_info.get_obj_info(texture_envs["_TexCb"]["m_Texture"]["m_PathID"], root_mono_behaviour).obj.image
    obj_cr = export_info.get_obj_info(texture_envs["_TexCr"]["m_Texture"]["m_PathID"], root_mono_behaviour).obj.image
    obj_a = export_info.get_obj_info(texture_envs["_TexA"]["m_Texture"]["m_PathID"], root_mono_behaviour).obj.image

    return obj_y, obj_cb, obj_cr, obj_a


def crop_parts_image(
        export_info: "ExportInfo", img: Image, parts_table: list[dict[str, dict[str, int]]],
        image_name: str, container: str
) -> Image:
    """
    Crop the parts image of ``img`` according to ``parts_table``.

    If no position data is provided in ``parts_table``, default coordinates will be used instead.
    """
    is_using_default = False
    log("DEBUG", f"Cropping image part of {image_name}... ({container})")

    # size = (tl_x, tl_y, rb_x, rb_y)
    if not parts_table:
        if WarningType.NO_PARTS_INFO not in export_info.suppressed_warnings:
            log("WARNING", f"{image_name} ({container}) does not have parts, using default positions")

        # Use default coordinates because parts table not available
        size = (296, 21, 808, 533)  # 512 x 512
        is_using_default = True
    else:
        # Use data from parts table
        parts_position = parts_table[0]["position"]
        center_x, center_y = parts_position["x"], parts_position["y"]
        size = (center_x - 128, center_y - 128, center_x + 128, center_y + 128)

    img = crop_image(img, *size)

    if is_using_default:
        img = img.resize(_parts_image_size, Image.ANTIALIAS)

    return img


def export_image_story(export_info: "ExportInfo", /, crop_parts_base: bool = True) -> ExportResult:
    """
    Export the image objects in ``export_info`` with YCbCr channel merged.

    Parts base is also cropped if ``crop_parts_base`` is not specified or ``True``.
    """
    mono_behaviour = next(info for info in export_info.objects if info.obj.type == "MonoBehaviour")

    log("DEBUG", f"Reading mono behaviour data... ({mono_behaviour.container})")

    tree = mono_behaviour.obj.read_typetree()

    image_name = mono_behaviour.obj.name

    meterial_path_id = tree["basePartsData"]["material"]["m_PathID"]

    if not meterial_path_id:
        if WarningType.NO_MATERIAL not in export_info.suppressed_warnings:
            log("WARNING", f"Material not available for {image_name} ({mono_behaviour.container})")
        return ExportResult()

    try:
        channels = get_y_cb_cr_a_from_material(
            cast(Material, export_info.get_obj_info(meterial_path_id, mono_behaviour).obj),
            export_info,
            mono_behaviour
        )
    except KeyError as ex:
        raise ValueError(f"Asset {image_name} ({mono_behaviour.container}) has missing object") from ex

    log("INFO", f"Exporting story image of {image_name}... ({mono_behaviour.container})")
    export_dir = export_info.get_export_dir_of_obj(mono_behaviour)
    export_paths = []

    log("DEBUG", f"Merging YCbCr of {image_name}... ({mono_behaviour.container})")
    img = merge_y_cb_cr_a(*channels)

    log("DEBUG", f"Saving merged YCbCr image of {image_name}... ({mono_behaviour.container})")
    export_path_merged = os.path.join(export_dir, f"{image_name}{'-full' if crop_parts_base else ''}.png")
    export_paths.append(export_path_merged)
    img.save(export_path_merged)

    if not crop_parts_base:
        # Early terminate if not to crop the parts
        return ExportResult(exported_paths=export_paths)

    log("DEBUG", f"Cropping parts base of {image_name}... ({mono_behaviour.container})")
    img = crop_parts_image(export_info, img, tree["partsDataTable"], image_name, mono_behaviour.container)

    log("DEBUG", f"Saving parts base of {image_name}... ({mono_behaviour.container})")
    export_path_image = os.path.join(export_dir, f"{image_name}.png")
    export_paths.append(export_path_image)
    img.save(export_path_image)

    return ExportResult(exported_paths=export_paths)
