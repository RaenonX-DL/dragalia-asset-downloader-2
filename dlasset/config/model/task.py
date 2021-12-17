"""Asset exporting task model."""
import re
from abc import ABC
from dataclasses import dataclass, field
from typing import Pattern, cast

from dlasset.enums import WarningType
from .base import ConfigBase
from .types import ExportType

__all__ = ("AssetTask", "AssetRawTask", "AssetSubTask")


@dataclass
class AssetSubTask(ConfigBase):
    """Asset exporting sub task model."""

    name: str = field(init=False)
    container_regex: Pattern = field(init=False)
    type: ExportType = field(init=False)
    is_multi_locale: bool = field(init=False)
    export_dependency: bool = field(init=False)
    export_updated_file_index: bool = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.json_obj.get("name", "(No Name)")
        self.container_regex = re.compile(self.json_obj["container"])
        self.type = cast(ExportType, self.json_obj["type"])
        self.is_multi_locale = cast(bool, self.json_obj.get("isMultiLocale", False))
        self.export_dependency = cast(bool, self.json_obj.get("exportDependency", False))
        self.export_updated_file_index = cast(bool, self.json_obj.get("exportUpdatedFileIndex", False))

    def match_container(self, container: str) -> bool:
        """Check if the given ``container`` matches the filter."""
        return bool(re.search(self.container_regex, container))

    @property
    def title(self) -> str:
        """Get a string of the summary of this task."""
        return f"{self.name} - {self.type} ({'all locale' if self.is_multi_locale else 'master only'})"


@dataclass
class AssetTaskBase(ConfigBase, ABC):
    """Base class for asset exporting task model."""

    name: str = field(init=False)
    asset_regex: Pattern = field(init=False)
    tasks: tuple[AssetSubTask, ...] = field(init=False)
    suppress_warnings: tuple[WarningType, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.name = cast(str, self.json_obj["name"])
        self.asset_regex = re.compile(self.json_obj["asset"])
        self.tasks = tuple(AssetSubTask(task) for task in self.json_obj["tasks"])
        self.suppress_warnings = tuple(WarningType(type_) for type_ in self.json_obj.get("suppressWarnings", []))

    @property
    def title(self) -> str:
        """Get a string of the summary of this task."""
        return f"{self.name} ({self.asset_regex.pattern})"


@dataclass
class AssetTask(AssetTaskBase):
    """Asset exporting task model."""


@dataclass
class AssetRawTask(AssetTaskBase):
    """Raw asset exporting task model."""
