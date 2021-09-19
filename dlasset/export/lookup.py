"""Exporting function index."""
from dlasset.config import ExportType

from .functions import export_mono_behaviour
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS",)

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
}
