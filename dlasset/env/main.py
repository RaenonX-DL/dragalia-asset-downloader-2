"""Implementations for initializing the environment."""
import os.path
from dataclasses import dataclass

from dlasset.config import Config
from dlasset.const import MANIFEST_NAMES
from dlasset.enums import Locale
from dlasset.log import log, log_group_end, log_group_start
from .args import CliArgs

__all__ = ("init_env", "Environment")


@dataclass
class Environment:
    """Settings related to the environment."""

    args: CliArgs
    config: Config

    def manifest_asset_path_of_locale(self, locale: Locale) -> str:
        """Get the manifest asset path of ``locale``."""
        return os.path.join(self.manifest_asset_dir, MANIFEST_NAMES[locale])

    def manifest_asset_decrypted_path(self, locale: Locale) -> str:
        """Get the decrypted manifest asset path of ``locale``."""
        return f"{self.manifest_asset_path_of_locale(locale)}.decrypted"

    @property
    def manifest_asset_dir(self) -> str:
        """Directory of the encrypted manifest assets."""
        return os.path.join(self.config.paths.downloaded, "manifest", self.args.version_code)

    @property
    def assets_dir(self) -> str:
        """Directory of the assets."""
        return os.path.join(self.config.paths.downloaded, "assets")

    def print_info(self) -> None:
        """Print the info about the current environment."""
        log_group_start("Environment info")
        log("INFO", f"External library directory: {self.config.paths.lib}")
        log("INFO", "-" * 20)
        log("INFO", f"Manifest asset directory: {self.manifest_asset_dir}")
        log("INFO", f"Downloaded assets directory: {self.assets_dir}")
        log("INFO", f"Exported files directory: {self.config.paths.export}")
        log_group_end()


def init_env(args: CliArgs, config: Config) -> Environment:
    """Initializes the environment."""
    log_group_start("Environment initialization")
    env = Environment(args, config)

    # Make directories needed if not made yet
    log("INFO", "Making directory for manifest...")
    os.makedirs(env.manifest_asset_dir, exist_ok=True)
    log("INFO", "Making directory for assets...")
    os.makedirs(env.assets_dir, exist_ok=True)
    log("INFO", "Making directory for export...")
    os.makedirs(env.config.paths.export, exist_ok=True)

    log_group_end()

    return env
