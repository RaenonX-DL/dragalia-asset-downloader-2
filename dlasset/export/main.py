"""Implementations to export files from an Unity asset."""
import os
from typing import BinaryIO, Optional, Sequence, TypeVar

import UnityPy
from UnityPy.classes import Object

from dlasset.config import AssetTaskFilter, ExportType
from dlasset.log import log
from .lookup import EXPORT_FUNCTIONS, SELECT_FUNCTIONS
from .types import ExportReturn

__all__ = ("export_asset",)

T = TypeVar("T", bound=Object)


def export_object(
        obj: T, export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> Optional[ExportReturn]:
    """
    Export a single Unity asset ``obj`` to ``export_dir``.

    Returns ``None`` if the object name does not match any of the ``name`` regex pattern in ``filters``.
    """
    obj = obj.read()

    if filters and not any(filter_.match_name(obj.name) for filter_ in filters):
        return None

    log("INFO", f"Exporting {obj.name}...")

    os.makedirs(export_dir, exist_ok=True)

    return EXPORT_FUNCTIONS[obj.type.name](obj, export_dir)


def export_asset(
        asset_stream: BinaryIO,
        export_type: ExportType,
        export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ExportReturn]:
    """
    Export the unity asset with the given criteria to ``export_dir`` and get the exported data.

    Returns an empty list is nothing exportable.
    """
    asset_path = asset_stream.name
    asset_name = os.path.basename(asset_path)

    asset = UnityPy.load(asset_stream)

    log("INFO", f"Exporting asset: {asset_path}")
    log("INFO", f"Export type: {export_type}")
    log("INFO", f"Destination: {export_dir}")

    objects = asset.objects
    if not objects:
        log("WARNING", f"Nothing exportable for the asset: {asset_name}")
        return []

    objects_to_export = SELECT_FUNCTIONS[export_type](asset, filters)

    log("INFO", f"{len(objects_to_export)} out of {len(objects)} objects to export.")

    exported: list[ExportReturn] = []

    for obj in objects_to_export:
        exported_obj = export_object(obj, export_dir, filters=filters)
        if not exported_obj:
            continue

        exported.append(exported_obj)

    log("INFO", f"Done exporting {asset_name} to {export_dir}")

    return exported
