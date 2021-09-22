"""Implementations to export files from an Unity asset."""
from typing import Optional, Sequence

from dlasset.config import AssetSubTask, ExportType
from dlasset.enums import WarningType
from dlasset.log import log
from dlasset.manage import get_asset
from .lookup import EXPORT_FUNCTIONS, TYPES_TO_INCLUDE
from .model import ExportInfo
from .types import ExportReturn

__all__ = ("export_asset",)


def log_asset_export_debug_info(asset_paths: tuple[str, ...], export_type: ExportType, export_dir: str) -> None:
    """Log the debug info about the asset exporting."""
    log("DEBUG", "Exporting asset info:")
    for asset_path in asset_paths:
        log("DEBUG", f"- {asset_path}")
    log("DEBUG", f"Export type: {export_type}")
    log("DEBUG", f"Destination: {export_dir}")


def export_asset(
        asset_paths: tuple[str, ...],  # `list` won't allow multiprocessing because it's unhashable
        export_type: ExportType,
        export_dir: str, *,
        sub_task: Optional[AssetSubTask] = None,
        suppress_warnings: Sequence[WarningType] = ()
) -> ExportReturn:
    """
    Export the asset from ``asset_paths`` with the given criteria to ``export_dir`` and get the exported data.

    Returns ``None`` if nothing exportable or exported.
    """
    asset = get_asset(asset_paths)

    log_asset_export_debug_info(asset_paths, export_type, export_dir)

    log("DEBUG", f"Getting objects to export from {asset.asset_count} assets ({asset.name})...")

    objects_to_export = asset.get_objects_matching_filter(TYPES_TO_INCLUDE[export_type], sub_task=sub_task)

    if not objects_to_export:
        if WarningType.NOTHING_TO_EXPORT not in suppress_warnings:
            log("WARNING", f"Nothing to export for the asset: {asset.name}")
        return None

    log("INFO", f"Found {len(objects_to_export)} objects to export from {asset.name}.")

    export_info = ExportInfo(
        export_dir=export_dir, obj_info_list=objects_to_export, assets=asset, suppressed_warnings=suppress_warnings
    )
    results = EXPORT_FUNCTIONS[export_type](export_info)

    log("DEBUG", f"Done exporting {asset.name} to {export_dir}")

    return results
