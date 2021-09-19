"""Manifest file model classes."""
import re
from dataclasses import dataclass, field
from typing import Generator, Pattern

from dlasset.enums import Locale
from dlasset.export import MonoBehaviourTree
from dlasset.model import JsonModel

__all__ = ("Manifest", "ManifestLocale", "ManifestEntry")


@dataclass
class ManifestEntry(JsonModel):
    """Manifest entry model."""

    name: str = field(init=False)
    hash: str = field(init=False)
    dependencies: list[str] = field(init=False)
    size: int = field(init=False)
    group: int = field(init=False)
    assets: list[str] = field(init=False)

    hash_dir: str = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj["name"]
        self.hash = self.json_obj["hash"]
        self.dependencies = self.json_obj["dependencies"]
        self.size = self.json_obj["size"]
        self.group = self.json_obj["group"]
        self.assets = self.json_obj["assets"]

        self.hash_dir = self.hash[:2]


@dataclass
class ManifestCategory(JsonModel):
    """Manifest category model."""

    name: str = field(init=False)
    assets: tuple[ManifestEntry, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj["name"]
        self.assets = tuple(ManifestEntry(entry) for entry in self.json_obj["assets"])


@dataclass
class ManifestLocale(JsonModel):
    """Manifest model of a locale."""

    categories: tuple[ManifestCategory, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.categories = tuple(ManifestCategory(category) for category in self.json_obj["categories"])

    @property
    def entries_across_category(self) -> Generator[ManifestEntry, None, None]:
        """Get a generator yielding the manifest entries across categories."""
        return (asset for category in self.categories for asset in category.assets)


@dataclass
class Manifest:
    """Manifest model of all locales."""

    data: dict[Locale, MonoBehaviourTree]

    manifests: dict[Locale, ManifestLocale] = field(init=False)

    def __post_init__(self) -> None:
        self.manifests = {locale: ManifestLocale(manifest) for locale, manifest in self.data.items()}

    def get_entry_with_regex(
            self, regex: Pattern, *,
            is_master_only: bool
    ) -> Generator[tuple[Locale, ManifestEntry], None, None]:
        """Get the generator yielding the manifest entry with its name matching ``regex``."""
        for locale, manifest_of_locale in self.manifests.items():
            if is_master_only and not locale.is_master:
                continue

            for entry in manifest_of_locale.entries_across_category:
                if not re.match(regex, entry.name):
                    continue

                yield locale, entry
