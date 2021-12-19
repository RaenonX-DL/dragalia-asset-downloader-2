"""Global config model class."""
from dataclasses import dataclass, field
from typing import cast

from .base import ConfigBase

__all__ = ("Global",)


@dataclass
class Global(ConfigBase):
    """Various global settings."""

    export_updated_file_index: bool = field(init=False)

    def __post_init__(self) -> None:
        self.export_updated_file_index = cast(bool, self.json_obj.get("exportUpdatedFileIndex", False))
