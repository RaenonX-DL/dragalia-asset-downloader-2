"""Manifest entry model classes."""
from abc import ABC
from dataclasses import dataclass, field

from dlasset.model import JsonModel


@dataclass
class ManifestEntryBase(JsonModel, ABC):
    """Manifest entry model base."""

    name: str = field(init=False)
    hash: str = field(init=False)
    size: int = field(init=False)
    group: int = field(init=False)

    hash_dir: str = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj["name"]
        self.hash = self.json_obj["hash"]
        self.size = self.json_obj["size"]
        self.group = self.json_obj["group"]

        self.hash_dir = self.hash[:2]


@dataclass
class ManifestEntry(ManifestEntryBase):
    """Manifest entry model."""

    dependencies: list[str] = field(init=False)
    assets: list[str] = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.dependencies = self.json_obj["dependencies"]
        self.assets = self.json_obj["assets"]


@dataclass
class ManifestRawEntry(ManifestEntryBase):
    """Manifest entry model for raw assets."""
