"""Utils functions for managing the assets."""
from typing import TYPE_CHECKING

from dlasset.const import CDN_BASE_URL

if TYPE_CHECKING:
    from dlasset.manifest import ManifestEntry

__all__ = ("get_asset_url",)


def get_asset_url(entry: "ManifestEntry") -> str:
    """Get the URL of the manifest ``entry``."""
    return f"{CDN_BASE_URL}/assetbundles/Android/{entry.hash_dir}/{entry.hash}"
