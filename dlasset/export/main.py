"""Implementations to export files from an Unity asset."""
import os
from typing import Optional, Sequence

from dlasset.config import AssetTaskFilter, ExportType
from dlasset.enums import WarningType
from dlasset.log import log
from dlasset.manage import get_asset
from dlasset.model import ObjectInfo, UnityAsset
from .lookup import EXPORT_FUNCTIONS, TYPES_TO_INCLUDE
from .model import ExportInfo
from .types import ExportReturn

__all__ = ("export_asset",)


def log_asset_export_debug_info(asset_paths: list[str], export_type: ExportType, export_dir: str) -> None:
    """Log the debug info about the asset exporting."""
    log("DEBUG", "Exporting asset:")
    for asset_path in asset_paths:
        log("DEBUG", f"- {asset_path}")
    log("DEBUG", f"Export type: {export_type}")
    log("DEBUG", f"Destination: {export_dir}")


def get_objects_to_export(
        assets: list[UnityAsset], export_type: ExportType, *,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ObjectInfo]:
    """
    Get a list of objects to export from all ``assets``.

    Note that ``filters`` only apply on the main asset, the 1st asset in ``assets``.
    """
    obj_export: list[ObjectInfo] = []

    for idx, asset in enumerate(assets):
        obj_export.extend(asset.get_objects_matching_filter(
            TYPES_TO_INCLUDE[export_type],
            filters=filters if idx == 0 else None
        ))

    return obj_export


def export_objects(
        obj_info_list: list[ObjectInfo], export_type: ExportType, export_dir: str, *,
        asset_name: str,
) -> list[ExportReturn]:
    """
    Export the objects in ``obj_info_list``.

    Note that ``filters`` are only apply to the objects coming from the main asset.
    """
    export_info = ExportInfo(export_dir=export_dir, obj_info_list=obj_info_list, asset_name=asset_name)
    results = EXPORT_FUNCTIONS[export_type](export_info)

    if not results:
        return []

    return results


def export_asset(
        asset_paths: list[str],
        export_type: ExportType,
        export_dir: str, *,
        filters: Optional[Sequence[AssetTaskFilter]] = None,
        suppress_warnings: Sequence[WarningType] = ()
) -> Optional[list[ExportReturn]]:
    """
    Export the asset from ``asset_paths`` with the given criteria to ``export_dir`` and get the exported data.

    Returns ``None`` if nothing exportable or exported.
    """
    assets = [get_asset(asset_path) for asset_path in asset_paths]

    asset_path_main = asset_paths[0]
    asset_name_main = os.path.basename(asset_path_main)

    log_asset_export_debug_info(asset_paths, export_type, export_dir)

    log("DEBUG", "Getting objects to export...")

    objects_to_export = get_objects_to_export(assets, export_type, filters=filters)

    if not objects_to_export and WarningType.NOTHING_TO_EXPORT not in suppress_warnings:
        log("WARNING", f"Nothing to export for the asset: {asset_name_main}")
        return None

    log("INFO", f"Found {len(objects_to_export)} objects to export ({asset_path_main}).")

    results: list[ExportReturn] = export_objects(
        objects_to_export, export_type, export_dir,
        asset_name=asset_name_main
    )

    log("DEBUG", f"Done exporting {asset_name_main} to {export_dir}")

    return results
