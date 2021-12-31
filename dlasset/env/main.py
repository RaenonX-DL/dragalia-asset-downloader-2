"""Implementations for initializing the environment."""
import os.path
import shutil
from dataclasses import dataclass, field
from datetime import datetime

from dlasset.config import Config
from dlasset.const import MANIFEST_NAMES
from dlasset.enums import Locale
from dlasset.log import init_log, log, log_group_end, log_group_start
from .args import CliArgs
from .index import FileIndex

__all__ = ("init_env", "Environment")


@dataclass
class Environment:
    """Settings related to the environment."""

    args: CliArgs
    config: Config

    index: FileIndex = field(init=False)

    init_time: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.index = FileIndex(
            index_dir=self.config.paths.index,
            version_code=self.args.version_code,
            enabled=not self.args.no_index,
            export_updated=self.config.global_.export_updated_file_index,
            export_updated_dir=self.config.paths.updated
        )

        self.init_time = datetime.utcnow()

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

        if self.args.no_index:
            log("WARNING", "File indexing is not enabled. Files matching the task criteria will be downloaded.")

        log("INFO", f"Version code: {self.args.version_code}")
        log("INFO", f"Config file path: {self.args.config_path}")
        log("INFO", "-" * 20)
        log("INFO", f"External library directory: {self.config.paths.lib}")
        if self.config.concurrency.processes:
            log("INFO", f"Max processes to use: {self.config.concurrency.processes}")
        if self.config.concurrency.batch_size:
            log("INFO", f"Task batch size: {self.config.concurrency.batch_size}")
        log("INFO", "-" * 20)
        log("INFO", f"Manifest asset directory: {self.manifest_asset_dir}")
        log("INFO", f"Downloaded assets directory: {self.downloaded_assets_dir}")
        log("INFO", f"Exported files directory: {self.config.paths.export}")
        log("INFO", f"File index directory: {self.config.paths.index}")
        log("INFO", f"Log root directory: {self.config.paths.log}")
        log("INFO", "-" * 20)
        log("INFO", f"Disable file indexing: {self.args.no_index}")
        log("INFO", "Suppressed warnings:")
        for task in self.config.asset_tasks:
            if not task.suppress_warnings:
                continue

            log("INFO", f"{task.title}:")
            for warning_type in task.suppress_warnings:
                log("INFO", f"- {warning_type}")

        log_group_end()

    def init_dirs(self) -> None:
        """Initialize directories."""
        self.config.paths.init_dirs()

        log("DEBUG", "Making directory for manifest assets...")
        os.makedirs(self.manifest_asset_dir, exist_ok=True)
        log("DEBUG", "Making directory for downloaded assets...")
        os.makedirs(self.downloaded_assets_dir, exist_ok=True)
        log("DEBUG", "Making directory for exported audio...")
        os.makedirs(self.config.audio_task.export_dir, exist_ok=True)

    def prepare_logging(self) -> None:
        """Prepare logging factory."""
        init_log(self.config.paths.log)

    def cleanup(self) -> None:
        """Perform cleanup tasks."""
        log_group_start("Clean Up")

        log("INFO", "Cleaning up temp file directory...")
        shutil.rmtree(self.config.paths.temp)

        log_group_end()


def init_env(args: CliArgs, config: Config) -> Environment:
    """Initializes the environment."""
    log_group_start("Environment initialization")

    env = Environment(args, config)
    log("INFO", "Creating directories...")
    env.init_dirs()
    log("INFO", "Initializing logging...")
    env.prepare_logging()

    log_group_end()

    return env
