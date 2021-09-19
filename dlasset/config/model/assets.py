"""Asset exporting task model."""
from dataclasses import dataclass, field
from typing import Optional, cast

from .base import ConfigBase
from .types import ObjectType

__all__ = ("AssetTask",)


@dataclass
class AssetTaskFilter(ConfigBase):
    """Asset exporting task filter model."""

    container_regex: str = field(init=False)
    name_regex: Optional[str] = field(init=False)

    def __post_init__(self) -> None:
        self.container_regex = cast(str, self.json_obj["container"])
        self.name_regex = cast(Optional[str], self.json_obj.get("name"))


@dataclass
class AssetTask(ConfigBase):
    """Asset exporting task model."""

    name: str = field(init=False)
    asset_regex: str = field(init=False)
    types: tuple[ObjectType, ...] = field(init=False)
    conditions: tuple[AssetTaskFilter, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.name = cast(str, self.json_obj["task"])
        self.asset_regex = cast(str, self.json_obj["name"])
        self.types = cast(tuple[ObjectType], tuple(self.json_obj["types"]))
        self.conditions = tuple(AssetTaskFilter(filter_) for filter_ in self.json_obj["filter"])
