"""Implementations for exporting the decrypted manifest assets."""
from typing import cast

from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.export import MonoBehaviourTree, export_asset
from dlasset.log import log, log_group_end, log_group_start
from dlasset.utils import concurrent_run
from .model import Manifest

__all__ = ("export_manifest_all_locale",)


def export_manifest_of_locale(env: Environment, locale: Locale) -> MonoBehaviourTree:
    """Export and store the manifest file of ``locale``."""
    log("INFO", f"Exporting manifest of {locale}...")

    with open(env.manifest_asset_decrypted_path(locale), "rb") as f:
        exported = export_asset(f, ["MonoBehaviour"], env.config.paths.export_dir_of_locale(locale))

    # Manifest asset only contains one `MonoBehaviour`
    return exported[0]


def export_manifest_all_locale(env: Environment) -> Manifest:
    """
    Export and store the manifest file of all possible ``locale``.

    Also, returns the manifest file as model for each locale.
    """
    log_group_start("Manifest exporting")
    results = concurrent_run(
        export_manifest_of_locale, [[env, locale] for locale in Locale],
        key_of_call=lambda _, locale: cast(Locale, locale)
    )
    log_group_end()

    return Manifest(results)
