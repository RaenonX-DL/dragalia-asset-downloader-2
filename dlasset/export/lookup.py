"""Exporting function index."""
from dlasset.config import ExportType, UnityType
from .functions import (
    export_anim_ctrl, export_anim_override, export_game_object, export_image, export_image_alpha,
    export_image_story, export_mono_behaviour, export_sprite_ui,
)
from .types import ExportFunction

__all__ = ("EXPORT_FUNCTIONS", "TYPES_TO_INCLUDE")

EXPORT_FUNCTIONS: dict[ExportType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
    "Texture2D": export_image,
    "Texture2D-Alpha": export_image_alpha,
    "Texture2D-Story": export_image_story,
    "Sprite-UI": export_sprite_ui,
    "GameObject": export_game_object,
    "AnimatorController": export_anim_ctrl,
    "AnimatorOverrideController": export_anim_override,
}

TYPES_TO_INCLUDE: dict[ExportType, tuple[UnityType, ...]] = {
    "MonoBehaviour": ("MonoBehaviour",),
    "Texture2D": ("Texture2D",),
    "Texture2D-Alpha": ("Texture2D", "Material"),
    "Texture2D-Story": ("Texture2D", "Material", "MonoBehaviour"),
    "Sprite-UI": ("Sprite", "MonoBehaviour"),
    "GameObject": ("GameObject", "MonoBehaviour", "MonoScript"),
    "AnimatorController": ("AnimatorController",),
    "AnimatorOverrideController": ("AnimatorOverrideController",),
}
