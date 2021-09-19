"""Type definitions for exporting the assets."""
from typing import Callable, Literal, TypeVar

from UnityPy.classes import Object

__all__ = ("ObjectType", "ExportFunction")

ObjectType = Literal["MonoBehaviour"]

T = TypeVar("T", bound=Object)

ExportFunction = Callable[[T, str], None]
