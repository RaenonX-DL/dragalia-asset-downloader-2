"""Implementations to export files from an Unity asset."""
import os
from typing import Any, Sequence

import UnityPy

from dlasset.config import ObjectType
from dlasset.log import log
from .lookup import EXPORT_FUNCTIONS
from .types import ExportReturn

__all__ = ("export_asset",)


def export_asset(asset_path: str, types_to_export: Sequence[ObjectType], export_dir: str) -> list[ExportReturn]:
    """
    Export the unity asset with the given criteria to ``export_dir`` and get the exported data.

    Returns an empty list is nothing exportable.
    """
    asset = UnityPy.load(asset_path)

    log("INFO", f"Exporting asset: {asset_path}")
    log("INFO", f"Object Types: {types_to_export}")
    log("INFO", f"Destination: {export_dir}")

    objects = asset.objects
    if not objects:
        log("WARNING", f"Nothing exportable the asset at {asset_path}")
        return []

    exported: list[Any] = []
    for obj in objects:
        if obj.type not in types_to_export:
            continue

        obj = obj.read()
        log("INFO", f"Exporting {obj.type} at {asset.path} to {export_dir}")
        os.makedirs(export_dir, exist_ok=True)
        exported.append(EXPORT_FUNCTIONS[obj.type.name](obj, export_dir))

    asset_name = os.path.basename(asset_path)
    log("INFO", f"Done exporting {asset_name} to {export_dir}")

    return exported
