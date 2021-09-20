"""Asset exporting task model."""
import re
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional, Pattern, cast

from dlasset.enums import WarningType
from .base import ConfigBase
from .types import ExportType

__all__ = ("AssetTask", "AssetRawTask", "AssetTaskFilter")


@dataclass
class AssetTaskBase(ConfigBase, ABC):
    """Base class for asset exporting task model."""

    name: str = field(init=False)
    asset_regex: Pattern = field(init=False)
    is_multi_locale: bool = field(init=False)
    suppress_warnings: tuple[WarningType, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.name = cast(str, self.json_obj["task"])
        self.asset_regex = re.compile(self.json_obj["name"])
        self.is_multi_locale = cast(bool, self.json_obj.get("isMultiLocale", False))
        self.suppress_warnings = tuple(WarningType(type_) for type_ in self.json_obj.get("suppressWarnings", []))

    @property
    def title(self) -> str:
        """Get a string containg the summary of this task."""
        return f"{self.name} (Regex: {self.asset_regex.pattern} - " \
               f"{'all locale' if self.is_multi_locale else 'master only'})"


@dataclass
class AssetTaskFilter(ConfigBase):
    """Asset exporting task filter model."""

    container_regex: Pattern = field(init=False)
    name_regex: Optional[Pattern] = field(init=False)

    def __post_init__(self) -> None:
        self.container_regex = re.compile(self.json_obj["container"])

    def match_container(self, container: str) -> bool:
        """Check if the given ``container`` matches the filter."""
        return bool(re.search(self.container_regex, container))


@dataclass
class AssetTask(AssetTaskBase):
    """Asset exporting task model."""

    type: ExportType = field(init=False)
    conditions: tuple[AssetTaskFilter, ...] = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.types = cast(ExportType, self.json_obj["type"])
        self.conditions = tuple(AssetTaskFilter(filter_) for filter_ in self.json_obj["filter"])


@dataclass
class AssetRawTask(AssetTaskBase):
    """Raw asset exporting task model."""
