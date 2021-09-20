"""Main implementations for managing the assets."""
import os.path
from functools import lru_cache
from typing import TYPE_CHECKING

import requests

from dlasset.env import Environment
from dlasset.model import UnityAsset
from .utils import get_asset_url

if TYPE_CHECKING:
    from dlasset.manifest import ManifestEntry

__all__ = ("get_asset_paths", "get_asset")


def download_asset(asset_hash_dir: str, asset_target_path: str, entry: "ManifestEntry") -> None:
    """Download the asset of manifest ``entry`` and store it to ``asset_target_path``."""
    response = requests.get(get_asset_url(entry))

    os.makedirs(asset_hash_dir, exist_ok=True)
    with open(asset_target_path, "wb+") as f:
        f.write(response.content)


def get_asset_paths(env: Environment, entries: list["ManifestEntry"]) -> tuple[str, ...]:
    """
    Get a list of asset paths of ``entry``.

    This automatically download the asset in ``entries`` if not exists.
    """
    asset_paths: list[str] = []
    for entry in entries:
        asset_hash_dir = os.path.join(env.downloaded_assets_dir, entry.hash_dir)
        asset_target_path = os.path.join(asset_hash_dir, entry.hash)

        if not os.path.exists(asset_target_path):
            download_asset(asset_hash_dir, asset_target_path, entry)

        asset_paths.append(asset_target_path)

    return tuple(asset_paths)


@lru_cache(maxsize=100)
def get_asset(asset_paths: tuple[str]) -> UnityAsset:
    """Get the unity asset model at ``asset_paths``."""
    return UnityAsset(asset_paths)
