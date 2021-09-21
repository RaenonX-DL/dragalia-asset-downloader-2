"""Unity asset model."""
import os
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

import UnityPy
from UnityPy.classes import Object
from UnityPy.environment import Environment

from dlasset.log import log_periodic
from .obj import ObjectInfo

if TYPE_CHECKING:
    from dlasset.config import AssetSubTask, UnityType

__all__ = ("UnityAsset",)


@dataclass
class UnityAsset:
    """Unity asset model."""

    asset_paths: tuple[str]

    _assets: list[Environment] = field(init=False)

    _obj_dict: dict[int, Object] = field(init=False)
    _obj_info_cache: dict[int, ObjectInfo] = field(init=False)

    def __post_init__(self) -> None:
        self._assets = [UnityPy.load(asset_path) for asset_path in self.asset_paths]

        self._obj_dict = {}
        for asset in self._assets:
            self._obj_dict.update({obj.path_id: obj for obj in asset.objects})

        self._obj_info_cache = {}

    @property
    def asset_count(self) -> int:
        """Count of assets included in this model."""
        return len(self._assets)

    @property
    def main_path(self) -> str:
        """Get the path of the main asset (1st asset)."""
        return self.asset_paths[0]

    @property
    def name(self) -> str:
        """Get the name of this asset. This uses the main asset name as the name."""
        return os.path.basename(self.main_path)

    def get_obj_info_at_path_id(self, path_id: int, src_path: str) -> Optional[ObjectInfo]:
        """
        Get the object at ``path_id``.

        ``src_path`` is the path of the asset that requested to find a certain object.

        Returns ``None`` if no such object exists.
        """
        if obj_info := self._obj_info_cache.get(path_id):
            return obj_info

        if obj := self._obj_dict.get(path_id):
            ret = ObjectInfo(obj=obj.read(), container=src_path)
            self._obj_info_cache[path_id] = ret
            return ret

        return None

    def get_objects_matching_filter(
            self, types: tuple["UnityType", ...], *,
            sub_task: Optional["AssetSubTask"] = None
    ) -> list[ObjectInfo]:
        """
        Get a list of objects in type of ``types`` and match any of the given ``filters``.

        If ``filters`` is not provided or set to ``None``, all objects in type of ``types`` will be returned.

        Note that this only include objects coming from the main asset.
        Objects from the dependency assets are ignored.
        """
        ret: list[ObjectInfo] = []

        main_asset = self._assets[0]

        objects: list[tuple[str, Object]] = main_asset.container.items()

        object_count = len(objects)

        for idx, (path, obj) in enumerate(objects):
            if obj.type not in types:
                continue

            if sub_task and not sub_task.match_container(path):
                continue

            log_periodic("INFO", f"Reading {idx} / {object_count} ({idx / object_count:.2%}) objects")

            ret.append(ObjectInfo(obj=obj.read(), container=path))

        return ret
