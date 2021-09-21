"""Implementations for performing an asset exporting task."""
from typing import TYPE_CHECKING

from dlasset.config import AssetSubTask, AssetTask
from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manage import get_asset_paths
from dlasset.utils import concurrent_run_no_return
from .main import export_asset

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestEntry

__all__ = ("export_by_task",)


def export_from_manifest(
        env: Environment, locale: Locale, entries: list["ManifestEntry"],
        task: AssetTask, sub_task: AssetSubTask
) -> None:
    """Export the asset of ``entry`` according to ``task``."""
    asset_paths = get_asset_paths(env, entries)
    export_asset(
        asset_paths, sub_task.type, env.config.paths.export_asset_dir_of_locale(locale),
        sub_task=sub_task, suppress_warnings=task.suppress_warnings
    )


def export_by_task(env: Environment, manifest: "Manifest", task: AssetTask) -> None:
    """Export the assets according to ``task``."""
    processed_entries = []

    for sub_task in task.tasks:
        log_group_start(f"{task.title} // {sub_task.title}")

        log("INFO", "Getting asset entry from the manifest...")
        asset_entries = list(
            manifest.get_entry_with_regex(task.asset_regex, is_master_only=not sub_task.is_multi_locale)
        )
        args_list = [
            [env, locale, entries, task, sub_task] for locale, entries in asset_entries
            if any(env.index.is_file_updated(locale, entry) for entry in entries)
        ]

        log(
            "INFO",
            f"{len(asset_entries)} assets matching the criteria. "
            f"{len(args_list)} assets updated{' (force update)' if env.args.no_index else ''}."
        )

        concurrent_run_no_return(export_from_manifest, args_list, env.config.paths.log)

        processed_entries.extend(asset_entries)

        log_group_end()

    # MUST update outside of the concurrent run
    # Otherwise, the index will not update because of the separated memory space
    # ---------------------------------------------------------------------------------------
    # Update only if a task is completed, because subtasks are performed on the same asset(s)
    for locale, entries in processed_entries:
        for entry in entries:
            env.index.update_entry(locale, entry)
