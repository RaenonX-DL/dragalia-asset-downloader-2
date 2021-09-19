"""Implementations to export files from an Unity asset."""
import os
from typing import BinaryIO, Optional, Sequence, TypeVar

import UnityPy
from UnityPy.classes import Object

from dlasset.config import AssetTaskFilter, ExportType
from dlasset.log import log
from .lookup import EXPORT_FUNCTIONS
from .types import ExportReturn

__all__ = ("export_asset",)

T = TypeVar("T", bound=Object)


def export_asset(
        asset_stream: BinaryIO,
        export_type: ExportType,
        export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> Optional[ExportReturn]:
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
        return None

    log("INFO", f"{len(objects)} objects at max to export.")

    exported: ExportReturn = EXPORT_FUNCTIONS[export_type](asset, export_dir, filters)

    log("INFO", f"Done exporting {asset_name} to {export_dir}")

    return exported
