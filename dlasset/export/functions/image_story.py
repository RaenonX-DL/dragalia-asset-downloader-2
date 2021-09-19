"""Implementations to export story emotion image."""
import os
from typing import TYPE_CHECKING, cast

from PIL import Image
from UnityPy.classes import Material

from dlasset.log import log
from dlasset.utils import crop_image, merge_y_cb_cr_a

if TYPE_CHECKING:
    from dlasset.export import ExportInfoPathDict

__all__ = ("export_image_story",)


def get_y_cb_cr_a_from_material(
        material: Material,
        info_path_dict: "ExportInfoPathDict"
) -> tuple[Image, Image, Image, Image]:
    """Get a tuple containing Y, Cb, Cr, alpha image object in order of the material."""
    texture_envs = dict(material.read_typetree()["m_SavedProperties"]["m_TexEnvs"])

    obj_y = cast(Image, info_path_dict[texture_envs["_TexY"]["m_Texture"]["m_PathID"]].obj.image)
    obj_cb = cast(Image, info_path_dict[texture_envs["_TexCb"]["m_Texture"]["m_PathID"]].obj.image)
    obj_cr = cast(Image, info_path_dict[texture_envs["_TexCr"]["m_Texture"]["m_PathID"]].obj.image)
    obj_a = cast(Image, info_path_dict[texture_envs["_TexA"]["m_Texture"]["m_PathID"]].obj.image)

    return obj_y, obj_cb, obj_cr, obj_a


def export_image_story(info_path_dict: "ExportInfoPathDict") -> None:
    """Export the image objects in ``info_path_dict`` with YCbCr channel merged."""
    mono_behaviour = next(info for info in info_path_dict.values() if info.obj.type == "MonoBehaviour")

    log("DEBUG", f"Reading mono behaviour data... ({mono_behaviour.container})")

    tree = mono_behaviour.obj.read_typetree()

    parts_base_mat_path = tree["basePartsData"]["material"]["m_PathID"]
    parts_position = tree["partsDataTable"][0]["position"]

    channels = get_y_cb_cr_a_from_material(
        cast(Material, info_path_dict[parts_base_mat_path].obj),
        info_path_dict
    )

    image_name = mono_behaviour.obj.name

    log("INFO", f"Exporting {image_name}... ({mono_behaviour.container})")

    export_path = os.path.join(mono_behaviour.export_dir, f"{image_name}.png")

    log("DEBUG", f"Merging YCbCr of {image_name}... ({mono_behaviour.container})")

    img = merge_y_cb_cr_a(*channels)

    x, y = parts_position["x"], parts_position["y"]
    img = crop_image(img, x - 128, y - 128, x + 128, y + 128)

    img.save(export_path)
