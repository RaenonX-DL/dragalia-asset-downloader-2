"""Implementations to export ``MonoBehaviour``."""
import json
import os

import aiofiles
from UnityPy.classes import MonoBehaviour

from dlasset.log import log

__all__ = ("export_mono_behaviour",)


async def export_mono_behaviour(obj: MonoBehaviour, export_dir: str) -> None:
    """Export ``obj`` to ``export_dir``."""
    export_path: str = os.path.join(export_dir, f"{obj.name}.json")
    log("INFO", f"Exporting MonoBehaviour of {obj.name} to {export_path}")

    if obj.serialized_type.nodes:
        tree = obj.read_typetree()
        async with aiofiles.open(export_path, "w+", encoding="utf-8") as f:
            await f.write(json.dumps(tree, ensure_ascii=False, indent=2))
