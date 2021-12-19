"""Implementations for the file index."""
import json
import os.path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from dlasset.config import AssetSubTask, AssetTask
from dlasset.enums import Locale
from dlasset.utils import export_json
from .exportype import TaskEntry

if TYPE_CHECKING:
    from dlasset.export import ExportResult
    from dlasset.manifest import ManifestEntryBase

__all__ = ("FileIndex",)


@dataclass
class FileIndex:
    """File index model class."""

    index_dir: str
    enabled: bool

    export_updated: bool
    export_updated_dir: str

    _data: dict[Locale, dict[str, str]] = field(init=False)  # key = file name from entry; value = hash
    _updated: dict[Locale, list[tuple[AssetTask, list[tuple[AssetSubTask, "ExportResult"]]]]] = field(init=False)

    def _init_index_data(self, locale: Locale) -> None:
        index_file_path = self.get_index_file_path(locale)

        if not os.path.exists(index_file_path):
            # Index file not exists, create empty index
            self._data[locale] = {}
            return

        with open(index_file_path, "r", encoding="utf-8") as f:
            self._data[locale] = json.load(f)

    def _init_updated_index(self, locale: Locale) -> None:
        self._updated[locale] = []

    def __post_init__(self) -> None:
        self._data = {}
        self._updated = {}

        if not self.enabled:
            # Skip initializing index data if not enabled
            return

        for locale in Locale:
            self._init_index_data(locale)
            self._init_updated_index(locale)

    def get_index_file_path(self, locale: Locale) -> str:
        """Get the index file path of ``locale``."""
        return os.path.join(self.index_dir, f"index-{locale.value}.json")

    def get_updated_index_file_path(self) -> str:
        """Get the updated index file path."""
        return os.path.join(self.export_updated_dir, "updated.json")

    def is_file_updated(self, locale: Locale, entry: "ManifestEntryBase") -> bool:
        """Check if ``entry`` is updated."""
        if not self.enabled:
            # Always return ``True`` to force re-download if not enabled
            return True

        # File name not being in the index is considered as updated (should perform downloading tasks)
        if entry.name not in self._data[locale]:
            return True

        # Hash mismatch is considered as updated
        return self._data[locale][entry.name] != entry.hash

    def update_entry(
            self, locale: Locale, task: "AssetTask", entry: "ManifestEntryBase",
            export_results: list[tuple[AssetSubTask, "ExportResult"]]
    ) -> None:
        """Update ``entry`` in the index."""
        if not self.enabled:
            # Do nothing if not enabled
            return

        self._data[locale][entry.name] = entry.hash

        if self.export_updated or task.export_updated_file_index:
            self._updated[locale].append((task, export_results))

    def _export_index(self) -> None:
        for locale, data in self._data.items():
            file_path = self.get_index_file_path(locale)

            export_json(file_path, data, separators=(",", ":"))

    def _export_updated_index(self) -> None:
        export: dict[str, list[TaskEntry]] = {}
        file_path = self.get_updated_index_file_path()

        # Using `locale.value` instead of `locale` for json exporting
        for locale, task_results in self._updated.items():
            export[locale.value] = []

            for task, subtask_results in task_results:
                tasks: TaskEntry = {
                    "name": task.title,
                    "subtasks": []
                }

                for subtask, export_result in subtask_results:
                    tasks["subtasks"].append({
                        "name": subtask.title,
                        "paths": export_result.exported_paths
                    })

                export[locale.value].append(tasks)

        export_json(file_path, export, separators=(",", ":"))

    def update_index_files(self) -> None:
        """Push the updated file index to its corresponding file."""
        if not self.enabled:
            # Do nothing if not enabled
            return

        self._export_index()
        self._export_updated_index()
