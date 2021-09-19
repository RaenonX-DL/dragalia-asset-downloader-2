"""Implementations to export images such as ``Texture2D`` and ``Sprite``."""
import os
from typing import Optional, Sequence

from UnityPy.classes import Material
from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter

__all__ = ("export_image",)


def export_image(asset: UnityAsset, export_dir: str, filters: Optional[Sequence[AssetTaskFilter]] = None) -> None:
    """Export the image in ``asset`` to ``export_dir``."""
    materials: list[Material] = []

    for obj in asset.objects:
        # DON'T use `!=` because this is using `__eq__` override for comparison
        # `__ne__` is not properly overridden
        if obj.type not in ("Material",):
            continue

        if filters and not any(filter_.match_container(obj.container) for filter_ in filters):
            continue

        # create destination path
        export_path = os.path.join(export_dir, f"{+obj.name}.png")

        img = obj.image
        img.save(export_path)

        materials.append(obj)
