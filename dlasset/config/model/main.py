"""Main config model implementation."""
from dataclasses import dataclass, field
from typing import Any

from .paths import Paths

__all__ = ("Config",)


@dataclass
class Config:
    """Asset downloader config."""

    data: dict[Any, Any]

    paths: Paths = field(init=False)

    def __post_init__(self) -> None:
        self.paths = Paths(self.data["paths"])
