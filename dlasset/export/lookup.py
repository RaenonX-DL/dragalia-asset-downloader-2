"""Exporting function index."""
from .functions import export_mono_behaviour
from .types import ExportFunction, ObjectType

__all__ = ("EXPORT_FUNCTIONS",)

EXPORT_FUNCTIONS: dict[ObjectType, ExportFunction] = {
    "MonoBehaviour": export_mono_behaviour,
}
