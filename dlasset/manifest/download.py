"""Implementations to download manifest assets."""
import requests

from dlasset.const import CDN_BASE_URL, MANIFEST_NAMES
from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.utils import concurrent_run_no_return

__all__ = ("download_manifest_all_locale",)


def download_manifest_of_locale(env: Environment, locale: Locale) -> None:
    """
    Download and store the manifest asset of ``locale``.

    Downloaded asset needs decryption.
    """
    log("INFO", f"Downloading manifest of {locale}...")
    manifest_url = f"{CDN_BASE_URL}/manifests/Android/{env.args.version_code}/{MANIFEST_NAMES[locale]}"

    with requests.get(manifest_url) as response, open(env.manifest_asset_path_of_locale(locale), mode="wb+") as f:
        f.write(response.content)


def download_manifest_all_locale(env: Environment) -> None:
    """
    Download and store the manifest asset of all possible ``locale``.

    Downloaded asset needs decryption.
    """
    log_group_start("Manifest downloading")
    concurrent_run_no_return(download_manifest_of_locale, [[env, locale] for locale in Locale])
    log_group_end()
