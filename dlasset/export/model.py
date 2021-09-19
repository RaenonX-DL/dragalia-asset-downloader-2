"""Various model classes."""
import os
from dataclasses import dataclass

from UnityPy.classes import Object

__all__ = ("ExportInfo",)


@dataclass
class ExportInfo:
    """Export info model class."""

    export_dir: str
    container: str
    obj: Object

    def __post_init__(self) -> None:
        self.export_dir = os.path.join(self.export_dir, os.path.dirname(os.path.normpath(self.container)))
        # If the export info is created, it's likely that there are some things to be exported there
        os.makedirs(self.export_dir, exist_ok=True)

    def read_obj(self) -> Object:
        """
        Read the object.

        Note that this also changes the class attribute ``obj``.
        """
        self.obj = self.obj.read()
        return self.obj
