"""Various model classes."""
import os
from dataclasses import InitVar, dataclass, field
from functools import cache
from typing import Iterable

from UnityPy.classes import Object

__all__ = ("ExportInfo", "ObjectInfo")


@dataclass(unsafe_hash=True)
class ObjectInfo:
    """Object info model class."""

    obj: Object
    container: str
    is_from_main: bool

    def read_obj(self) -> Object:
        """
        Read the object.

        This modified the class attribute ``obj``.
        """
        self.obj = self.obj.read()
        return self.obj


@dataclass
class ExportInfo:
    """Export info model class."""

    export_dir: str
    obj_info_list: InitVar[list[ObjectInfo]]
    asset_name: str
    container_fallback: str

    _object_dict: dict[int, ObjectInfo] = field(init=False)

    def __post_init__(self, obj_info_list: list[ObjectInfo]) -> None:
        self._object_dict = {obj_info.obj.path_id: obj_info for obj_info in obj_info_list}

    def __hash__(self) -> int:
        return hash((self.export_dir, self.asset_name))

    def __repr__(self):
        return f"{self.asset_name} ({self.container_fallback})"

    @property
    def objects(self) -> Iterable[ObjectInfo]:
        """Get the objects to export."""
        return self._object_dict.values()

    def get_obj_info(self, path_id: int) -> ObjectInfo:
        """
        Get the object info at ``path_id``.

        Raises :class:`ValueError` if no corresponding object.
        """
        if path_id not in self._object_dict:
            raise ValueError(f"Path ID #{path_id} not exists on {self.asset_name} ({self.container_fallback})")

        return self._object_dict[path_id]

    @cache
    def get_export_dir_of_obj(self, obj_info: Object) -> str:
        """Get the export directory of ``obj_info``."""
        obj_export_dir = os.path.join(self.export_dir, os.path.dirname(os.path.normpath(obj_info.container)))
        os.makedirs(obj_export_dir, exist_ok=True)

        return obj_export_dir
