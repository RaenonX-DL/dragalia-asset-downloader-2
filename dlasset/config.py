"""Implementations to load the config file."""
import json
import typing
from dataclasses import dataclass
from typing import Any, cast

import yaml
from jsonschema import ValidationError, validate  # type: ignore

__all__ = ("load_config",)


@dataclass
class Config:
    """Asset downloader config."""


@typing.no_type_check
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

    return Config()
