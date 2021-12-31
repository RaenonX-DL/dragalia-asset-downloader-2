"""Manifest entry model classes."""
import os
from abc import ABC
from dataclasses import dataclass, field

from dlasset.env import Environment
from dlasset.model import JsonModel

__all__ = ("ManifestEntry", "ManifestRawEntry", "ManifestEntryBase",)


@dataclass
class ManifestEntryBase(JsonModel, ABC):
    """Manifest entry model base."""

    name: str = field(init=False)
    hash: str = field(init=False)
    size: int = field(init=False)
    group: int = field(init=False)

    dependencies: list[str] = field(init=False)

    hash_dir: str = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj["name"]
        self.hash = self.json_obj["hash"]
        self.size = self.json_obj["size"]
        self.group = self.json_obj["group"]

        self.dependencies = self.json_obj.get("dependencies", [])

        self.hash_dir = self.hash[:2]

    def get_actual_asset_dir(self, env: Environment):
        return os.path.join(env.downloaded_assets_dir, self.hash_dir)

    def get_asset_path(self, env: Environment):
        asset_hash_dir = self.get_actual_asset_dir(env)
        return os.path.join(asset_hash_dir, self.hash)


@dataclass
class ManifestEntry(ManifestEntryBase):
    """Manifest entry model."""

    assets: list[str] = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.assets = self.json_obj["assets"]


@dataclass
class ManifestRawEntry(ManifestEntryBase):
    """Manifest entry model for raw assets."""
