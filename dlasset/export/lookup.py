"""Exporting function index."""
from dlasset.config import ExportType
from .functions import export_image, export_mono_behaviour, select_mono_behaviour
from .types import ExportFunction, SelectFunction

__all__ = ("SELECT_FUNCTIONS", "EXPORT_FUNCTIONS",)

SELECT_FUNCTIONS: dict[ExportType, SelectFunction] = {
    "MonoBehaviour": select_mono_behaviour,
}

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
    "Texture2D": export_image,
    "Sprite": export_image,
}
