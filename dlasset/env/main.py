"""Implementations for initializing the environment."""
import logging
import os.path
from dataclasses import dataclass, field

from dlasset.config import Config
from dlasset.const import MANIFEST_NAMES
from dlasset.enums import Locale
from dlasset.log import PIDFileHandler, log, log_group_end, log_group_start
from .args import CliArgs
from .index import FileIndex

__all__ = ("init_env", "Environment")


@dataclass
class Environment:
    """Settings related to the environment."""

    args: CliArgs
    config: Config

    index: FileIndex = field(init=False)

    def __post_init__(self) -> None:
        self.index = FileIndex(self.config.paths.index)

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
    def downloaded_assets_dir(self) -> str:
        """Directory of the downloaded assets."""
        return os.path.join(self.config.paths.downloaded, "assets")

    def print_info(self) -> None:
        """Print the info about the current environment."""
        log_group_start("Environment info")
        log("INFO", f"External library directory: {self.config.paths.lib}")
        log("INFO", "-" * 20)
        log("INFO", f"Manifest asset directory: {self.manifest_asset_dir}")
        log("INFO", f"Downloaded assets directory: {self.downloaded_assets_dir}")
        log("INFO", f"Exported files directory: {self.config.paths.export}")
        log("INFO", f"File index directory: {self.config.paths.index}")
        log_group_end()

    def init_dirs(self) -> None:
        """Initialize directories."""
        self.config.paths.init_dirs()

        log("INFO", "Making directory for manifest assets...")
        os.makedirs(self.manifest_asset_dir, exist_ok=True)
        log("INFO", "Making directory for downloaded assets...")
        os.makedirs(self.downloaded_assets_dir, exist_ok=True)

    def prepare_logging(self) -> None:
        """Prepare logging factory."""
        logging.getLogger().addHandler(PIDFileHandler(self.config.paths.log))


def init_env(args: CliArgs, config: Config) -> Environment:
    """Initializes the environment."""
    log_group_start("Environment initialization")

    env = Environment(args, config)
    env.init_dirs()
    env.prepare_logging()

    log_group_end()

    return env
