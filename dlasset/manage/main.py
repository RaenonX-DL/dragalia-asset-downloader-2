"""Main implementations for managing the assets."""
import contextlib
import os.path
from typing import BinaryIO, Generator, TYPE_CHECKING

import requests

from dlasset.env import Environment
from .utils import get_asset_url

if TYPE_CHECKING:
    from dlasset.manifest import ManifestEntry

__all__ = ("asset_stream",)


def download_asset(asset_hash_dir: str, asset_target_path: str, entry: "ManifestEntry") -> None:
    """Download the asset of manifest ``entry`` and store it to ``asset_target_path``."""
    response = requests.get(get_asset_url(entry))

    os.makedirs(asset_hash_dir, exist_ok=True)
    with open(asset_target_path, "wb+") as f:
        f.write(response.content)


@contextlib.contextmanager
def asset_stream(env: Environment, entry: "ManifestEntry") -> Generator[BinaryIO, None, None]:
    """Get the asset stream of ``entry``."""
    asset_hash_dir = os.path.join(env.downloaded_assets_dir, entry.hash_dir)
    asset_target_path = os.path.join(asset_hash_dir, entry.hash)

    if not os.path.exists(asset_target_path):
        download_asset(asset_hash_dir, asset_target_path, entry)

    with open(asset_target_path, "rb") as f:
        yield f