"""Implementations for initializing the environment."""
import os.path
from dataclasses import dataclass

from dlasset.args import CliArgs
from dlasset.config import Config
from dlasset.const import MANIFEST_NAMES
from dlasset.enums import Locale
from dlasset.log import log, log_group_end, log_group_start

__all__ = ("init_env", "Environment")


@dataclass
class Environment:
    """Settings related to the environment."""

    args: CliArgs
    config: Config

    def manifest_asset_path_of_locale(self, locale: Locale) -> str:
        """Get the manifest asset path of ``locale``."""
        return os.path.join(self.manifest_asset_dir, MANIFEST_NAMES[locale])

    @property
    def manifest_asset_dir(self) -> str:
        """Directory of the encrypted manifest assets."""
        return os.path.join(self.config.paths.downloaded, "manifest", self.args.version_code)

    @property
    def assets_dir(self) -> str:
        """Directory of the assets."""
        return os.path.join(self.config.paths.downloaded, "assets")


def init_env(args: CliArgs, config: Config) -> Environment:
    """Initializes the environment."""
    log_group_start("Environment initialization")
    env = Environment(args, config)

    # Make directory for the assets if not made yet
    log("INFO", "Making directory for manifest...")
    os.makedirs(env.manifest_asset_dir, exist_ok=True)
    log("INFO", "Making directory for assets...")
    os.makedirs(env.assets_dir, exist_ok=True)

    log_group_end()

    return env
