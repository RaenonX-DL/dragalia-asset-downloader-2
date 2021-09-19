"""Implementations to export files from an Unity asset."""
import os
from typing import Sequence

import UnityPy

from dlasset.log import log
from .lookup import EXPORT_FUNCTIONS
from .types import ObjectType

__all__ = ("export_asset",)


async def export_asset(asset_path: str, types_to_export: Sequence[ObjectType], export_dir: str):
    """Export the unity asset with the given criteria to ``export_dir``."""
    asset = UnityPy.load(asset_path)

    log("INFO", f"Exporting asset: {asset_path}")
    log("INFO", f"Object Types: {types_to_export}")
    log("INFO", f"Destination: {export_dir}")

    objects = asset.objects
    if not objects:
        log("WARNING", f"Nothing exportable the asset at {asset_path}")
        return

    for obj in objects:
        if obj.type not in types_to_export:
            continue

        obj = obj.read()
        log("INFO", f"Exporting {obj.type} at {asset.path} to {export_dir}")
        os.makedirs(export_dir, exist_ok=True)
        await EXPORT_FUNCTIONS[obj.type.name](obj, export_dir)
