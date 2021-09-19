"""Implementations for exporting the decrypted manifest assets."""
import asyncio

from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.export import export_asset
from dlasset.log import log, log_group_end, log_group_start

__all__ = ("export_manifest_all_locale",)


async def export_manifest_of_locale(env: Environment, locale: Locale) -> None:
    """Export and store the manifest file of ``locale``."""
    log("INFO", f"Exporting manifest of {locale}...")

    await export_asset(
        env.manifest_asset_decrypted_path(locale),
        ["MonoBehaviour"],
        env.config.paths.export_dir_of_locale(locale)
    )


async def export_manifest_all_locale(env: Environment) -> None:
    """Export and store the manifest file of all possible ``locale``."""
    log_group_start("Manifest exporting")
    result = await asyncio.gather(*(export_manifest_of_locale(env, locale) for locale in Locale))
    log_group_end()
