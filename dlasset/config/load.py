"""Implementations to load the config file."""
import json
from typing import Any, cast

import yaml
from jsonschema import ValidationError, validate

from .model import Config

__all__ = ("load_config",)


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

    return Config(config)
