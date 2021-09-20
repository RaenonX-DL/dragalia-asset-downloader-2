"""Manifest categorical model class."""
from dataclasses import dataclass, field

from dlasset.model import JsonModel
from .entry import ManifestEntry


@dataclass
class ManifestCategory(JsonModel):
    """Manifest category model."""

    name: str = field(init=False)
    assets: tuple[ManifestEntry, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj["name"]
        self.assets = tuple(ManifestEntry(entry) for entry in self.json_obj["assets"])
