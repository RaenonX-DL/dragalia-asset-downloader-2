"""Various model classes."""
import os
from collections import Counter
from dataclasses import InitVar, dataclass, field
from functools import cache
from typing import Iterable, Sequence

from UnityPy.classes import Object

from dlasset.enums import WarningType
from dlasset.model import ObjectInfo, UnityAsset

__all__ = ("ExportInfo",)


@dataclass
class ExportInfo:
    """Export info model class."""

    export_dir: str
    obj_info_list: InitVar[list[ObjectInfo]]
    assets: UnityAsset
    suppressed_warnings: Sequence[WarningType]

    _object_info_dict: dict[int, ObjectInfo] = field(init=False)
    _object_info_cache: dict[int, ObjectInfo] = field(init=False)
    _main_container: str = field(init=False)

    def __post_init__(self, obj_info_list: list[ObjectInfo]) -> None:
        self._object_info_dict = {obj_info.obj.path_id: obj_info for obj_info in obj_info_list}
        self._object_info_cache = self._object_info_dict.copy()
        self._main_container = Counter(obj_info.container for obj_info in obj_info_list).most_common(1)[0][0]

    def __hash__(self) -> int:
        return hash((self.export_dir, self.asset_name))

    def __repr__(self) -> str:
        return f"{self.asset_name} ({self._main_container})"

    @property
    def objects(self) -> Iterable[ObjectInfo]:
        """Get the objects to export."""
        return self._object_info_dict.values()

    @property
    def asset_name(self) -> str:
        """Get the main asset name."""
        return self.assets.name

    def get_obj_info(self, path_id: int, src_obj_info: ObjectInfo) -> ObjectInfo:
        """
        Get the object info at ``path_id``.

        Raises :class:`ValueError` if no corresponding object.

        ``src_obj_info`` is the source object info that requested to find a certain object.

        This will try to search from the underlying asset if it's not found from ``obj_info_list``.
        """
        if path_id in self._object_info_cache:
            return self._object_info_cache[path_id]

        if obj_info := self.assets.get_obj_info_at_path_id(path_id, src_obj_info.container):
            self._object_info_cache[path_id] = obj_info
            return obj_info

        raise ValueError(f"Path ID #{path_id} not exists on {self}")

    @cache
    def get_export_dir_of_obj(self, obj_info: Object) -> str:
        """Get the export directory of ``obj_info``."""
        obj_export_dir = os.path.join(self.export_dir, os.path.dirname(os.path.normpath(obj_info.container)))
        os.makedirs(obj_export_dir, exist_ok=True)

        return obj_export_dir
