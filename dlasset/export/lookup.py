"""Exporting function index."""
from dlasset.config import ExportType
from .functions import export_image, export_mono_behaviour
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS",)

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
    "Texture2D": export_image,
    "Sprite": export_image,
}
