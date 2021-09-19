"""Exporting function index."""
from dlasset.config import ExportType, UnityType
from .functions import export_image, export_mono_behaviour
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS", "TYPES_TO_INCLUDE")

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
    "Texture2D": export_image,
    "Sprite": export_image,
}

TYPES_TO_INCLUDE: dict[ExportType, tuple[UnityType, ...]] = {
    "MonoBehaviour": ("MonoBehaviour",),
    "Texture2D": ("Texture2D",),
    "Sprite": ("Sprite",)
}
