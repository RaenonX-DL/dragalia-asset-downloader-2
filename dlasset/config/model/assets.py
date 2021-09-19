"""Asset exporting task model."""
import re
from dataclasses import dataclass, field
from typing import Optional, Pattern, cast

from .base import ConfigBase
from .types import ObjectType

__all__ = ("AssetTask", "AssetTaskFilter")


@dataclass
class AssetTaskFilter(ConfigBase):
    """Asset exporting task filter model."""

    container_regex: Pattern = field(init=False)
    name_regex: Optional[Pattern] = field(init=False)

    def __post_init__(self) -> None:
        self.container_regex = re.compile(self.json_obj["container"])

        if name_regex := self.json_obj.get("name"):
            self.name_regex = re.compile(name_regex)
        else:
            self.name_regex = None

    def match_name(self, name: str) -> bool:
        """Check if the given ``name`` matches the filter."""
        if self.name_regex:
            return bool(re.search(self.name_regex, name))

        # `name_regex` not set, always match
        return True

    def match_container(self, container: str) -> bool:
        """Check if the given ``container`` matches the filter."""
        return bool(re.search(self.container_regex, container))


@dataclass
class AssetTask(ConfigBase):
    """Asset exporting task model."""

    name: str = field(init=False)
    asset_regex: Pattern = field(init=False)
    types: tuple[ObjectType, ...] = field(init=False)
    conditions: tuple[AssetTaskFilter, ...] = field(init=False)
    is_multi_locale: bool = field(init=False)

    def __post_init__(self) -> None:
        self.name = cast(str, self.json_obj["task"])
        self.asset_regex = re.compile(self.json_obj["name"])
        self.types = cast(tuple[ObjectType], tuple(self.json_obj["types"]))
        self.conditions = tuple(AssetTaskFilter(filter_) for filter_ in self.json_obj["filter"])
        self.is_multi_locale = cast(bool, self.json_obj.get("isMultiLocale", False))

    @property
    def title(self) -> str:
        """Get a string containg some info of this task."""
        return f"{self.name} (Regex: {self.asset_regex.pattern} - " \
               f"{'all locale' if self.is_multi_locale else 'master only'})"
