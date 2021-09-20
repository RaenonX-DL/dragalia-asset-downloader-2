"""Unity asset model."""
import os
from dataclasses import dataclass, field
from typing import Optional, Sequence, TYPE_CHECKING

import UnityPy
from UnityPy.environment import Environment

from dlasset.log import log_periodic
from .obj import ObjectInfo

if TYPE_CHECKING:
    from dlasset.config import AssetTaskFilter, UnityType

__all__ = ("UnityAsset",)


@dataclass
class UnityAsset:
    """Unity asset model."""

    asset_paths: tuple[str]

    _assets: list[Environment] = field(init=False)

    _obj_cache: dict[int, ObjectInfo] = field(init=False)

    def __post_init__(self) -> None:
        self._obj_dict = self.asset.objects

    def get_objects_matching_filter(
            self, types: tuple["UnityType", ...], *,
            filters: Optional[Sequence["AssetTaskFilter"]] = None
    ) -> list[ObjectInfo]:
        """
        Get a list of objects in type of ``types`` and match any of the given ``filters``.

        If ``filters`` is not provided or set to ``None``, all objects in type of ``types`` will be returned.
        """
        ret: list[ObjectInfo] = []

        objects = []
        for idx, asset in enumerate(self._assets):
            objects.extend([idx == 0, item] for item in asset.container.items())

        object_count = len(objects)

        for idx, (is_main, (path, obj)) in enumerate(objects):
            if obj.type not in types:
                continue

            if is_main and filters and not any(filter_.match_container(path) for filter_ in filters):
                continue

            obj = obj.read()

            log_periodic("INFO", f"Reading {idx} / {object_count} ({idx / object_count:.2%}) objects")

            ret.append(ObjectInfo(obj=obj, container=path))

        return ret
