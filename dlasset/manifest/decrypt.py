"""Implementations for decrypting the manifest assets."""
# The usage of `subprocess` is safe
import subprocess  # nosec

from dlasset.enums import Locale
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.utils import concurrent_run

__all__ = ("decrypt_manifest_all_locale",)


def decrypt_manifest_of_locale(env: Environment, locale: Locale) -> None:
    """Decrypt and store the manifest asset of ``locale``."""
    log("INFO", f"Decrypting manifest of {locale}...")

    path_encrypted = env.manifest_asset_path_of_locale(locale)
    path_decrypted = env.manifest_asset_decrypted_path(locale)

    # Already listed `dotnet` as prerequisites for running this script (relative executable path)
    # Inputs are presumably sanitized
    subprocess.run(  # nosec
        [
            "dotnet",
            env.config.paths.lib_decrypt_dll_path,
            path_encrypted,
            path_decrypted,
            env.args.key,
            env.args.iv,
        ],
        check=True
    )


def decrypt_manifest_all_locale(env: Environment) -> None:
    """Decrypt and store the manifest asset of all locales."""
    log_group_start("Manifest decrypting")
    concurrent_run(decrypt_manifest_of_locale, [[env, locale] for locale in Locale])
    log_group_end()
