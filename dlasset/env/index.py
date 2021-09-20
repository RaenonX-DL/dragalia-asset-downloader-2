"""Implementations for the file index."""
import json
import os.path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from dlasset.enums import Locale
from dlasset.utils import export_json

if TYPE_CHECKING:
    from dlasset.manifest import ManifestEntryBase

__all__ = ("FileIndex",)


@dataclass
class FileIndex:
    """File index model class."""

    index_dir: str
    enabled: bool

    _data: dict[Locale, dict[str, str]] = field(init=False)  # key = file name from entry; value = hash

    def __post_init__(self) -> None:
        self._data = {}

        if not self.enabled:
            # Skip initializing index data if not enabled
            return

        for locale in Locale:
            index_file_path = self.get_index_file_path(locale)

            if not os.path.exists(index_file_path):
                # Index file not exists, create empty index
                self._data[locale] = {}
                continue

            with open(index_file_path, "r", encoding="utf-8") as f:
                self._data[locale] = json.load(f)

    def get_index_file_path(self, locale: Locale) -> str:
        """Get the index file path of ``locale``."""
        return os.path.join(self.index_dir, f"index-{locale.value}.json")

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

    def update_entry(self, locale: Locale, entry: "ManifestEntryBase") -> None:
        """Update ``entry`` in the index."""
        if not self.enabled:
            # Do nothing if not enabled
            return

        self._data[locale][entry.name] = entry.hash

    def update_index_files(self) -> None:
        """Push the updated file index to its corresponding file."""
        if not self.enabled:
            # Do nothing if not enabled
            return

        for locale, data in self._data.items():
            file_path = self.get_index_file_path(locale)

            export_json(file_path, data, separators=(",", ":"))
