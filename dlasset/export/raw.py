"""Implementations for exporting raw assets."""
import sys

from dlasset.config import AssetRawTask
from dlasset.env import Environment
from dlasset.log import log, log_group_end, log_group_start
from dlasset.manifest import Manifest

__all__ = ("export_raw_by_task",)


def export_raw_by_task(_: Environment, __: Manifest, task: AssetRawTask) -> None:
    """Export raw assets according to ``task``."""
    log_group_start(task.title)

    log("ERROR", "Raw task extraction not implemented")

    log_group_end()

    sys.exit(1)
