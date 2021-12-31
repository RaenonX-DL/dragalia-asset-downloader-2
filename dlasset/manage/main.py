"""Main implementations for managing the assets."""
import os.path
from functools import lru_cache
from typing import Sequence, TYPE_CHECKING

from dlasset.env import Environment
from dlasset.model import UnityAsset
from dlasset.utils import http_get
from .utils import get_asset_url

if TYPE_CHECKING:
    from dlasset.manifest import ManifestEntryBase

__all__ = ("get_asset_paths", "get_asset")


def download_asset(asset_hash_dir: str, asset_target_path: str, entry: "ManifestEntryBase") -> None:
    """Download the asset of manifest ``entry`` and store it to ``asset_target_path``."""
    response = http_get(get_asset_url(entry))

    os.makedirs(asset_hash_dir, exist_ok=True)
    with open(asset_target_path, "wb+") as f:
        f.write(response.content)


def get_asset_paths(env: Environment, entries: Sequence["ManifestEntryBase"]) -> tuple[str, ...]:
    """
    Get a list of asset paths of ``entries``.

    This automatically download the asset in ``entries`` if not exists.
    """
    asset_paths: list[str] = []
    for entry in entries:
        asset_target_path = entry.get_asset_path(env)

        if not os.path.exists(asset_target_path):
            download_asset(entry.get_actual_asset_dir(env), asset_target_path, entry)

        asset_paths.append(asset_target_path)

    return tuple(asset_paths)


@lru_cache(maxsize=100)
def get_asset(asset_paths: tuple[str]) -> UnityAsset:
    """Get the unity asset model at ``asset_paths``."""
    return UnityAsset(asset_paths)
