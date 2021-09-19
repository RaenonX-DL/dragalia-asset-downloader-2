"""Implementations for performing an asset exporting task."""
from typing import TYPE_CHECKING

from dlasset.config import AssetTask
from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manage import asset_stream
from dlasset.utils import concurrent_run_no_return
from .main import export_asset

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestEntry

__all__ = ("export_by_task",)


def export_from_manifest(env: Environment, locale: Locale, entry: "ManifestEntry", task: AssetTask) -> None:
    """Export the asset of ``entry`` according to ``task``."""
    log("INFO", f"Exporting {entry.name}...")
    with asset_stream(env, entry) as f:
        export_asset(f, task.types, env.config.paths.export_asset_dir_of_locale(locale), filters=task.conditions)

    env.index.update_entry(locale, entry)


def export_by_task(env: Environment, manifest: "Manifest", task: AssetTask) -> None:
    """Export the assets according to ``task``."""
    log_group_start(task.title)

    log("INFO", f"Types of object to export: {task.types}")

    log("INFO", "Filtering assets...")
    asset_entries = list(manifest.get_entry_with_regex(task.asset_regex, is_master_only=not task.is_multi_locale))
    args_list = [
        [env, locale, entry, task] for locale, entry in asset_entries
        if env.index.is_file_updated(locale, entry)
    ]
    log("INFO", f"{len(asset_entries)} assets matching the criteria. {len(args_list)} assets updated.")

    concurrent_run_no_return(export_from_manifest, args_list)

    log_group_end()
