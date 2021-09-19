"""Implementations to export files from an Unity asset."""
import os
from collections import Counter
from typing import BinaryIO, Optional, Sequence

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
        asset: UnityAsset, export_type: ExportType, export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ExportInfo]:
    """Get the info of the objects in ``asset`` to export."""
    export_info: list[ExportInfo] = []

    container_fallback: str = Counter(asset.container.keys()).most_common(1)[0][0]

    for obj in asset.objects:
        # `__ne__` not properly overridden, so `!=` doesn't work
        if obj.type not in TYPES_TO_INCLUDE[export_type]:
            continue

        container = obj.container or container_fallback
        if filters and not any(filter_.match_container(container) for filter_ in filters):
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


def export_asset(
        asset_stream: BinaryIO,
        export_type: ExportType,
        export_dir: str, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> Optional[list[ExportReturn]]:
    """
    Export the unity asset with the given criteria to ``export_dir`` and get the exported data.

    Returns an empty list is nothing exportable.
    """
    asset_path = asset_stream.name
    asset_name = os.path.basename(asset_path)

    asset = UnityPy.load(asset_stream)

    log("DEBUG", f"Exporting asset: {asset_path}")
    log("DEBUG", f"Export type: {export_type}")
    log("DEBUG", f"Destination: {export_dir}")

    objects = asset.objects
    if not objects:
        log("WARNING", f"Nothing exportable for the asset: {asset_name}")
        return None

    log("DEBUG", "Getting objects to export...")
    export_info_list = get_export_info_list(asset, export_type, export_dir, filters=filters)
    if not export_info_list:
        log("INFO", f"Nothing to export for the asset: {asset_name}")
        return None

    log("INFO", f"Found {len(export_info_list)} out of {len(objects)} exportable objects ({asset_path}).")

    results: list[ExportReturn] = export_objects(export_info_list, export_type, filters=filters)

    log("DEBUG", f"Done exporting {asset_name} to {export_dir}")

    return results
