"""Implementations for performing an asset exporting task."""
from typing import TYPE_CHECKING

from dlasset.config import AssetTask
from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manage import get_asset_paths
from dlasset.utils import concurrent_run_no_return
from .main import export_asset

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestEntry

__all__ = ("export_by_task",)


def export_from_manifest(env: Environment, locale: Locale, entries: list["ManifestEntry"], task: AssetTask) -> None:
    """Export the asset of ``entry`` according to ``task``."""
    log("INFO", f"Exporting ({len(entries)}) {entries[0].name}...")
    asset_paths = get_asset_paths(env, entries)
    export_asset(asset_paths, task.types, env.config.paths.export_asset_dir_of_locale(locale), filters=task.conditions)


def export_by_task(env: Environment, manifest: "Manifest", task: AssetTask) -> None:
    """Export the assets according to ``task``."""
    log_group_start(task.title)

    log("DEBUG", f"Types of object to export: {task.types}")

    log("INFO", "Filtering assets...")
    asset_entries = list(manifest.get_entry_with_regex(task.asset_regex, is_master_only=not task.is_multi_locale))
    args_list = [
        [env, locale, entries, task] for locale, entries in asset_entries
        if any(env.index.is_file_updated(locale, entry) for entry in entries)
    ]
    log("INFO", f"{len(asset_entries)} assets matching the criteria. {len(args_list)} assets updated.")

    concurrent_run_no_return(export_from_manifest, args_list, env.config.paths.log)

    # MUST update outside of the concurrent run
    # Otherwise the index will not update because of the separated memory space
    for locale, entries in asset_entries:
        for entry in entries:
            env.index.update_entry(locale, entry)

    log_group_end()
