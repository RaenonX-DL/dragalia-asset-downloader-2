"""Concurrency config model class."""
from dataclasses import dataclass, field
from typing import Optional

from .base import ConfigBase

__all__ = ("Concurrency",)


@dataclass
class Concurrency(ConfigBase):
    """Various concurrency settings."""

    processes: Optional[int] = field(init=False)
    batch_size: Optional[int] = field(init=False)

    def __post_init__(self) -> None:
        self.processes = self.json_obj.get("processes")
        self.batch_size = self.json_obj.get("batchSize")
