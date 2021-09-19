"""Exporting function index."""
from dlasset.config import ObjectType

from .functions import export_mono_behaviour
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS",)

EXPORT_FUNCTIONS: dict[ObjectType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
}
