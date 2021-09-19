"""Manifest file model classes."""
from dataclasses import dataclass, field
from typing import Any

from dlasset.enums import Locale
from dlasset.export import MonoBehaviourTree

__all__ = ("Manifest", "ManifestLocale")


@dataclass
class ManifestEntry:
    """Manifest entry model."""

    data: dict[Any, Any]

    name: str = field(init=False)
    hash: str = field(init=False)
    dependencies: list[str] = field(init=False)
    size: int = field(init=False)
    group: int = field(init=False)
    assets: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.data["name"]
        self.hash = self.data["hash"]
        self.dependencies = self.data["dependencies"]
        self.size = self.data["size"]
        self.group = self.data["group"]
        self.assets = self.data["assets"]


@dataclass
class ManifestCategory:
    """Manifest category model."""

    data: dict[Any, Any]

    name: str = field(init=False)
    assets: list[ManifestEntry] = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.data["name"]
        self.assets = self.data["assets"]


@dataclass
class ManifestLocale:
    """Manifest model of a locale."""

    data: MonoBehaviourTree

    categories: list[ManifestCategory] = field(init=False)

    def __post_init__(self) -> None:
        self.categories = self.data["categories"]


@dataclass
class Manifest:
    """Manifest model of all locales."""

    data: dict[Locale, MonoBehaviourTree]

    manifests: dict[Locale, ManifestLocale] = field(init=False)

    def __post_init__(self) -> None:
        self.manifests = {locale: ManifestLocale(manifest) for locale, manifest in self.data.items()}
