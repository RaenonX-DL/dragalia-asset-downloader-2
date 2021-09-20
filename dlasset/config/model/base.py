"""Base config object class."""
from abc import ABC
from dataclasses import dataclass

from dlasset.model import JsonModel

__all__ = ("ConfigBase",)


# https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class ConfigBase(JsonModel, ABC):
    """Base class of a config data."""
