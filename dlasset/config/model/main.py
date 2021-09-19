"""Main config model implementation."""
from dataclasses import dataclass, field

from .assets import AssetTask
from .base import ConfigBase
from .paths import Paths

__all__ = ("Config",)


@dataclass
class Config(ConfigBase):
    """Asset downloader config."""

    paths: Paths = field(init=False)
    asset_tasks: tuple[AssetTask, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.paths = Paths(self.json_obj["paths"])
        self.asset_tasks = tuple(AssetTask(task) for task in self.json_obj["assets"])
