"""Exporting function index."""
from dlasset.config import ExportType, UnityType
from .functions import export_image, export_image_alpha, export_image_story, export_mono_behaviour
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS", "TYPES_TO_INCLUDE")

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
    "Texture2D": export_image,
    "Texture2D-Alpha": export_image_alpha,
    "Texture2D-Story": export_image_story,
    "Sprite": export_image,
}

TYPES_TO_INCLUDE: dict[ExportType, tuple[UnityType, ...]] = {
    "MonoBehaviour": ("MonoBehaviour",),
    "Texture2D": ("Texture2D",),
    "Texture2D-Alpha": ("Texture2D", "Material"),
    "Texture2D-Story": ("Texture2D", "Material", "MonoBehaviour"),
    "Sprite": ("Sprite",)
}
