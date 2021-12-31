"""Implementations for performing an asset exporting task."""
from collections import defaultdict
from typing import Any, DefaultDict, Sequence, TYPE_CHECKING

from dlasset.config import AssetSubTask, AssetTask
from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manage import get_asset_paths
from dlasset.utils import concurrent_run
from .main import export_asset

if TYPE_CHECKING:
    from dlasset.manifest import Manifest, ManifestEntryBase
    from dlasset.export import ExportResult

__all__ = ("export_by_task",)

SingleTaskExportResult = DefaultDict[Locale, DefaultDict[AssetSubTask, list["ExportResult"]]]


def export_from_manifest(
        env: Environment, locale: Locale, entries: Sequence["ManifestEntryBase"],
        task: AssetTask, sub_task: AssetSubTask,
        *_: list[Any]
        # For allowing but ignoring additional args,
        # which might be needed for carrying more information in lazy call
) -> "ExportResult":
    """Export the asset of ``entry`` according to ``task``."""
    asset_paths = get_asset_paths(env, entries)

    return export_asset(
        asset_paths, sub_task.type, env.config.paths.export_asset_dir_of_locale(locale),
        sub_task=sub_task, suppress_warnings=task.suppress_warnings
    )


def export_by_task(env: Environment, manifest: "Manifest", task: AssetTask) -> None:
    """Export the assets according to ``task``."""
    processed_entries = []
    export_results: SingleTaskExportResult = defaultdict(lambda: defaultdict(list))

    for sub_task in task.tasks:
        log_group_start(f"{task.title} // {sub_task.title}")

        log("INFO", "Getting asset entry from the manifest...")
        asset_entries = list(
            manifest.get_entry_with_regex(task.asset_regex, is_master_only=not sub_task.is_multi_locale)
        )
        args_list = [
            [env, locale, entries, task, sub_task, idx] for idx, (locale, entries) in enumerate(asset_entries)
            if any(env.index.is_file_updated(locale, entry) for entry in entries)
        ]

        log(
            "INFO",
            f"{len(asset_entries)} assets matching the criteria. "
            f"{len(args_list)} assets updated{' (force update)' if env.args.no_index else ''}."
        )

        for (locale, _), export_result in concurrent_run(
                export_from_manifest, args_list, env.config.paths.log,
                # This carryies `locale` via concurrent result key
                key_of_call=lambda *args: (args[1], args[5]),
                max_workers=env.config.concurrency.processes,
                task_batch_size=env.config.concurrency.batch_size,
        ).items():
            export_results[locale][sub_task].append(export_result)

        processed_entries.extend(asset_entries)

        log_group_end()

    # MUST update outside the concurrent run
    # Otherwise, the index will not update because it's in a separated memory space
    # ---------------------------------------------------------------------------------------
    # Update only if a task is completed, because subtasks are performed on the same asset(s)
    for locale, entries in processed_entries:
        for entry in entries:
            env.index.update_entry(locale, task, entry, export_results[locale])
