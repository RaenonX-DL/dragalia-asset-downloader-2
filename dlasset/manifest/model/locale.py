"""Manifest model class of a locale."""
from dataclasses import dataclass, field
from typing import Generator

from dlasset.model import JsonModel
from .category import ManifestCategory
from .entry import ManifestEntry, ManifestRawEntry


@dataclass
class ManifestLocale(JsonModel):
    """Manifest model of a locale."""

    categories: tuple[ManifestCategory, ...] = field(init=False)
    raw_assets: tuple[ManifestRawEntry, ...] = field(init=False)

    entry_by_name: dict[str, ManifestEntry] = field(init=False)

    def __post_init__(self) -> None:
        self.categories = tuple(ManifestCategory(category) for category in self.json_obj["categories"])
        self.raw_assets = tuple(ManifestRawEntry(asset) for asset in self.json_obj["rawAssets"])

        self.entry_by_name = {entry.name: entry for entry in self.entries_across_category}

    @property
    def entries_across_category(self) -> Generator[ManifestEntry, None, None]:
        """Get a generator yielding the manifest entries across categories."""
        return (asset for category in self.categories for asset in category.assets)
