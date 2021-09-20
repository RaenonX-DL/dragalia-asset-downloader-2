"""Object info model class."""
from dataclasses import dataclass

from UnityPy.classes import Object

__all__ = ("ObjectInfo",)


@dataclass(unsafe_hash=True)
class ObjectInfo:
    """Object info model class."""

    obj: Object
    container: str
