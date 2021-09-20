"""Unity asset model."""
from dataclasses import dataclass, field
from typing import Optional, Sequence, TYPE_CHECKING

from UnityPy.classes import Object
from UnityPy.environment import Environment

from .obj import ObjectInfo

if TYPE_CHECKING:
    from dlasset.config import AssetTaskFilter, UnityType

__all__ = ("UnityAsset",)


@dataclass
class UnityAsset:
    """Unity asset model."""

    assets: Environment

    _obj_dict: dict[int, Object] = field(init=False)

    def __post_init__(self) -> None:
        self._obj_dict = self.assets.objects

    def get_objects_matching_filter(
            self, types: tuple["UnityType", ...], *,
            filters: Optional[Sequence["AssetTaskFilter"]] = None
    ) -> list[ObjectInfo]:
        """
        Get a list of objects in type of ``types`` and match any of the given ``filters``.

        If ``filters`` is not provided or set to ``None``, all objects in type of ``types`` will be returned.
        """
        ret: list[ObjectInfo] = []
        for path, obj in self.assets.container.items():
            if obj.type not in types:
                continue

            if filters and not any(filter_.match_container(path) for filter_ in filters):
                continue

            obj = obj.read()

            ret.append(ObjectInfo(obj=obj, container=path))

        return ret
