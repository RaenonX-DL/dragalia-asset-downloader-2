"""Main config model implementation."""
from dataclasses import dataclass, field

from .base import ConfigBase
from .paths import Paths
from .task import AssetRawTask, AssetTask

__all__ = ("Config",)


@dataclass
class Config(ConfigBase):
    """Asset downloader config."""

    paths: Paths = field(init=False)
    asset_tasks: tuple[AssetTask, ...] = field(init=False)
    raw_tasks: tuple[AssetRawTask, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.paths = Paths(self.json_obj["paths"])
        self.asset_tasks = tuple(AssetTask(task) for task in self.json_obj["assets"])
        self.raw_tasks = tuple(AssetRawTask(task) for task in self.json_obj["raw"])
