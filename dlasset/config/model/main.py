"""Main config model implementation."""
from dataclasses import dataclass, field
from typing import Optional

from .base import ConfigBase
from .concurrency import Concurrency
from .global_ import Global
from .paths import Paths
from .task import AssetAudioTask, AssetTask

__all__ = ("Config",)


@dataclass
class Config(ConfigBase):
    """Asset downloader config."""

    paths: Paths = field(init=False)
    concurrency: Concurrency = field(init=False)
    asset_tasks: tuple[AssetTask, ...] = field(init=False)
    audio_task: Optional[AssetAudioTask] = field(init=False)

    def __post_init__(self) -> None:
        self.paths = Paths(self.json_obj["paths"])
        self.concurrency = Concurrency(self.json_obj.get("concurrency", {}))
        self.global_ = Global(self.json_obj.get("global", {}))
        self.asset_tasks = tuple(AssetTask(task) for task in self.json_obj["assets"])
        self.audio_task = AssetAudioTask(self.json_obj["audio"]) if "audio" in self.json_obj else None
