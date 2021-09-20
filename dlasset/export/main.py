"""Implementations to export files from an Unity asset."""
import os
from typing import Optional, Sequence

from UnityPy.environment import Environment as UnityAsset

from dlasset.config import AssetTaskFilter, ExportType
from dlasset.enums import WarningType
from dlasset.log import log
from dlasset.manage import get_asset
from .lookup import EXPORT_FUNCTIONS, TYPES_TO_INCLUDE
from .model import ExportInfo, ObjectInfo
from .types import ExportReturn

__all__ = ("export_asset",)


def log_asset_export_debug_info(
        assets: list[UnityAsset], asset_paths: list[str], export_type: ExportType, export_dir: str
) -> None:
    """Log the debug info about the asset exporting."""
    log("DEBUG", "Exporting asset:")
    for asset_path in asset_paths:
        log("DEBUG", f"- {asset_path}")
    log("DEBUG", f"Export type: {export_type}")
    log("DEBUG", f"Destination: {export_dir}")
    log("DEBUG", f"Fallback Container: {get_container_fallback(assets)}")


def get_container_fallback(assets: list[UnityAsset]) -> str:
    """Get the fallback container to use for ``assets``."""
    main_asset = assets[0]

    # Pick the 1st container in the main asset
    return next(iter(main_asset.container.keys()))


def get_objects_to_export_of_asset(
        asset: UnityAsset, export_type: ExportType, /,
        container_fallback: str, is_main_asset: bool,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ObjectInfo]:
    """
    Get a list of objects to export in ``asset``.

    ``filters`` are omitted if ``is_main_asset`` is ``True``.
    """
    obj_export: list[ObjectInfo] = []

    for obj in asset.objects:
        # `__ne__` not properly overridden, so `!=` doesn't work
        if obj.type not in TYPES_TO_INCLUDE[export_type]:
            continue

        container = obj.container or container_fallback
        if is_main_asset and filters and not any(filter_.match_container(container) for filter_ in filters):
            return []

        obj_export.append(ObjectInfo(obj=obj, container=container, is_from_main=is_main_asset))

    return obj_export


def get_objects_to_export(
        assets: list[UnityAsset], export_type: ExportType, /,
        filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ObjectInfo]:
    """Get a list of objects to export from all ``assets``."""
    obj_export: list[ObjectInfo] = []

    container_fallback = get_container_fallback(assets)

    for idx, asset in enumerate(assets):
        if not asset.objects:
            continue

        obj_export.extend(get_objects_to_export_of_asset(
            asset, export_type,
            container_fallback=container_fallback, filters=filters, is_main_asset=idx == 0,
        ))

    return obj_export


def export_objects(
        obj_export: list[ObjectInfo], export_type: ExportType, export_dir: str, /,
        asset_name: str, container_fallback: str, filters: Optional[Sequence[AssetTaskFilter]] = None
) -> list[ExportReturn]:
    """
    Export the objects in ``obj_export``.

    Note that ``filters`` are only apply to the objects coming from the main asset.
    """
    obj_info_to_export: list[ObjectInfo] = []

    for obj_info in obj_export:
        obj = obj_info.read_obj()

        if (
                obj_info.is_from_main
                and filters
                and not any(filter_.match_filter(obj_info.container, obj.name) for filter_ in filters)
        ):
            continue

        obj_info_to_export.append(obj_info)

    export_info = ExportInfo(
        export_dir=export_dir,
        obj_info_list=obj_info_to_export,
        asset_name=asset_name,
        container_fallback=container_fallback
    )
    results = EXPORT_FUNCTIONS[export_type](export_info)

    if not results:
        return []

    return results


def export_asset(
        asset_paths: list[str],
        export_type: ExportType,
        export_dir: str, /,
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

    log_asset_export_debug_info(assets, asset_paths, export_type, export_dir)

    if not any(asset.objects for asset in assets) and WarningType.NOTHING_TO_EXPORT not in suppress_warnings:
        log("WARNING", f"Nothing exportable for the asset: {asset_name_main}")
        return None

    log("DEBUG", "Getting objects to export...")

    objects_to_export = get_objects_to_export(assets, export_type, filters=filters)

    if not objects_to_export and WarningType.NOTHING_TO_EXPORT not in suppress_warnings:
        log("WARNING", f"Nothing to export for the asset: {asset_name_main}")
        return None

    log("INFO", f"Found {len(objects_to_export)} objects to export ({asset_path_main}).")

    results: list[ExportReturn] = export_objects(
        objects_to_export, export_type, export_dir,
        filters=filters, asset_name=asset_name_main, container_fallback=get_container_fallback(assets)
    )

    log("DEBUG", f"Done exporting {asset_name_main} to {export_dir}")

    return results
