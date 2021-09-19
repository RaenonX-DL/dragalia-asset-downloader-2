"""Implementations to export files from an Unity asset."""
import os
from typing import Optional, Sequence

import UnityPy
from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter, ExportType
from dlasset.log import log
from .lookup import EXPORT_FUNCTIONS, TYPES_TO_INCLUDE
from .model import ExportInfo
from .types import ExportReturn
from .utils import get_export_info_path_dict

__all__ = ("export_asset",)


def get_export_info_list(
        asset: UnityAsset, export_type: ExportType, container: str, export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ExportInfo]:
    """Get the info of the objects in ``asset`` to export."""
    if filters and not any(filter_.match_container(container) for filter_ in filters):
        return []

    export_info: list[ExportInfo] = []

    for obj in asset.objects:
        # `__ne__` not properly overridden, so `!=` doesn't work
        if obj.type not in TYPES_TO_INCLUDE[export_type]:
            continue

        export_info.append(ExportInfo(export_dir=export_dir, obj=obj, container=container))

    return export_info


def export_objects(
        export_info_list: list[ExportInfo], export_type: ExportType, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ExportReturn]:
    """Export the objects in ``export_info_list``."""
    # Get the export info list for export
    to_export: list[ExportInfo] = []
    for export_info in export_info_list:
        obj = export_info.read_obj()

        if filters and not any(filter_.match_filter(export_info.container, obj.name) for filter_ in filters):
            continue

        to_export.append(export_info)

    results = EXPORT_FUNCTIONS[export_type](get_export_info_path_dict(to_export))
    if not results:
        return []

    return results


def log_asset_export_debug_info(asset_paths: list[str], export_type: ExportType, export_dir: str) -> None:
    """Log the debug info about the asset exporting."""
    log("DEBUG", "Exporting asset:")
    for asset_path in asset_paths:
        log("DEBUG", f"- {asset_path}")
    log("DEBUG", f"Export type: {export_type}")
    log("DEBUG", f"Destination: {export_dir}")


def get_container(assets: list[UnityAsset]) -> str:
    """Get the container to use for ``assets``."""
    main_asset = assets[0]

    if len(main_asset.container) > 1:
        raise ValueError(f"Asset at {main_asset.path} has 1 or more containers")

    return next(iter(main_asset.container.keys()))


def export_asset(
        asset_paths: list[str],
        export_type: ExportType,
        export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> Optional[list[ExportReturn]]:
    """
    Export the asset from ``asset_paths`` with the given criteria to ``export_dir`` and get the exported data.

    Returns ``None`` if nothing exportable or exported.
    """
    assets = [UnityPy.load(asset_path) for asset_path in asset_paths]

    asset_path_main = asset_paths[0]
    asset_name_main = os.path.basename(asset_path_main)

    log_asset_export_debug_info(asset_paths, export_type, export_dir)

    if not any(asset.objects for asset in assets):
        log("WARNING", f"Nothing exportable for the asset: {asset_name_main}")
        return None

    log("DEBUG", "Getting objects to export...")

    export_info_list = []
    for idx, asset in enumerate(assets):
        if not asset.objects:
            continue

        export_info_list.extend(get_export_info_list(
            asset, export_type, get_container(assets), export_dir, filters=None if idx == 0 else filters
        ))

    if not export_info_list:
        log("WARNING", f"Nothing to export for the asset: {asset_name_main}")
        return None

    log("INFO", f"Found {len(export_info_list)} objects to export ({asset_path_main}).")

    results: list[ExportReturn] = export_objects(export_info_list, export_type, filters=filters)

    log("DEBUG", f"Done exporting {asset_name_main} to {export_dir}")

    return results
