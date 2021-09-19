"""Type definitions for exporting the assets."""
from asyncio import Future
from typing import Callable, Literal

from UnityPy.classes import Object

__all__ = ("ObjectType", "ExportFunction")

ObjectType = Literal["MonoBehaviour"]

ExportFunction = Callable[[Object, str], Future]
