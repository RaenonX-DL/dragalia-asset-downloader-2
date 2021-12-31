"""Config path model class."""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast

from dlasset.enums import Locale
from dlasset.log import log
from .base import ConfigBase

__all__ = ("Paths",)


@dataclass
class Paths(ConfigBase):
    """Various paths for different types of data."""

    downloaded: str = field(init=False)
    lib: str = field(init=False)
    export: str = field(init=False)
    index: str = field(init=False)
    log: str = field(init=False)
    updated: str = field(init=False)
    temp: str = field(init=False)

    def __post_init__(self) -> None:
        self.downloaded = cast(str, os.path.normpath(self.json_obj["downloaded"]))
        self.lib = cast(str, os.path.normpath(self.json_obj["lib"]))
        self.export = cast(str, os.path.normpath(self.json_obj["export"]))
        self.index = cast(str, os.path.normpath(self.json_obj["index"]))

        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log = cast(str, os.path.normpath(os.path.join(self.json_obj["log"], today)))
        self.updated = cast(str, os.path.normpath(self.json_obj["updated"]))
        self.temp = cast(str, os.path.normpath(self.json_obj["temp"]))

    def export_asset_dir_of_locale(self, locale: Locale) -> str:
        """Get the root directory for the exported assets of ``locale``."""
        if locale.is_master:
            return self.export

        return os.path.join(self.export, "localized", locale.value)

    def init_dirs(self) -> None:
        """Initialize directories for output."""
        log("DEBUG", "Making directory for downloaded files...")
        os.makedirs(self.downloaded, exist_ok=True)

        log("DEBUG", "Making directory for exported files...")
        os.makedirs(self.export, exist_ok=True)

        log("DEBUG", "Making directory for file index...")
        os.makedirs(self.index, exist_ok=True)

        log("DEBUG", "Making directory for logs...")
        os.makedirs(self.log, exist_ok=True)

        log("DEBUG", "Making directory for updated file index...")
        os.makedirs(self.updated, exist_ok=True)

        log("DEBUG", "Making directory for temp files...")
        os.makedirs(self.temp, exist_ok=True)

    @property
    def lib_decrypt_dll_path(self) -> str:
        """Path of the DLL for decryption."""
        return os.path.join(self.lib, "decrypt", "Decrypt.dll")
