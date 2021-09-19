"""Config path model class."""
import os
from dataclasses import dataclass, field
from typing import cast

from dlasset.enums import Locale
from .base import ConfigBase

__all__ = ("Paths",)


@dataclass
class Paths(ConfigBase):
    """Various paths for different types of data."""

    downloaded: str = field(init=False)
    lib: str = field(init=False)
    export: str = field(init=False)

    def __post_init__(self) -> None:
        self.downloaded = cast(str, os.path.normpath(self.json_obj["downloaded"]))
        self.lib = cast(str, os.path.normpath(self.json_obj["lib"]))
        self.export = cast(str, os.path.normpath(self.json_obj["export"]))

    def export_dir_of_locale(self, locale: Locale) -> str:
        """Get the root directory for the exported assets of ``locale``."""
        if locale.is_master:
            return self.export

        return os.path.join(self.export, "localized", locale.value)

    @property
    def lib_decrypt_dll_path(self) -> str:
        """Path of the DLL for decryption."""
        return os.path.join(self.lib, "decrypt", "Decrypt.dll")
