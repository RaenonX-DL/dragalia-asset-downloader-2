"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import Union

from UnityPy.classes import Sprite, Texture2D

__all__ = ("export_image",)


def export_image(obj: Union[Texture2D, Sprite], export_dir: str) -> None:
    """Export the image in ``obj`` to ``export_dir``."""
    # create destination path
    export_path = os.path.join(export_dir, f"{+obj.name}.png")

    img = obj.image
    img.save(export_path)
