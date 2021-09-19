"""Implementations to load the config file."""
import json
import os.path
from dataclasses import InitVar, dataclass, field
from typing import Any, cast

import yaml
from jsonschema import ValidationError, validate

from dlasset.enums import Locale

__all__ = ("load_config", "Config")


@dataclass
class Paths:
    """Various paths for different types of data."""

    json_obj: InitVar[dict[Any, Any]]

    downloaded: str = field(init=False)
    lib: str = field(init=False)
    export: str = field(init=False)

    def __post_init__(self, json_obj: dict[Any, Any]) -> None:
        self.downloaded = cast(str, os.path.normpath(json_obj["downloaded"]))
        self.lib = cast(str, os.path.normpath(json_obj["lib"]))
        self.export = cast(str, os.path.normpath(json_obj["export"]))

    def export_dir_of_locale(self, locale: Locale) -> str:
        """Get the root directory for the exported assets of ``locale``."""
        if locale.is_master:
            return self.export

        return os.path.join(self.export, "localized", locale.value)

    @property
    def lib_decrypt_dll_path(self) -> str:
        """Path of the DLL for decryption."""
        return os.path.join(self.lib, "decrypt", "Decrypt.dll")


@dataclass
class Config:
    """Asset downloader config."""

    paths: Paths


def load_config(path: str) -> Config:
    """
    Load and validate the config.

    Raises :class:`ValueError` if the config schema doesn't match.
    """
    with open(path, encoding="utf-8") as f:
        config = cast(dict[Any, Any], yaml.safe_load(f))

    with open("config.schema.json", encoding="utf-8") as f:
        schema = cast(dict[Any, Any], json.load(f))

    try:
        validate(instance=config, schema=schema)
    except ValidationError as ex:
        raise ValueError("Config validation failed") from ex

    return Config(paths=Paths(config["paths"]))
