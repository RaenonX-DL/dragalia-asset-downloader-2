"""Main functions for logging."""
import logging
import os
import time
from typing import Any, Optional, cast

from .const import COLOR_RESET, LOG_LEVEL_COLOR, LOG_LEVEL_NUM, LogLevel

__all__ = ("log", "log_group_start", "log_group_end")

_GROUP_START_TIME: Optional[float] = None

_GROUP_CURRENT_NAME: Optional[str] = None


def log(level: LogLevel, message: Any) -> None:
    """Log ``message`` at ``level``."""
    logging.log(LOG_LEVEL_NUM[level], "%s%s%s", LOG_LEVEL_COLOR[level], message, COLOR_RESET)


def log_group_start(name: str) -> None:
    """
    Place a log group start marker with ``name``.

    Raises :class:`RuntimeError` if a group has not ended.
    """
    global _GROUP_CURRENT_NAME, _GROUP_START_TIME  # pylint: disable=global-statement
    if _GROUP_CURRENT_NAME is not None:
        raise RuntimeError(f"Group name: {_GROUP_CURRENT_NAME} has already started")

    _GROUP_START_TIME = time.time()
    _GROUP_CURRENT_NAME = name

    if os.environ.get("GITHUB_ACTIONS"):  # Environment variable to indicate that the s
        separator = f"::group::{name}"
    else:
        separator = f"{'-' * 20} {name} {'-' * 20}"

    print(separator)
    log("INFO", separator)


def log_group_end() -> None:
    """
    Place a group end marker.

    Raises :class:`RuntimeError` if currently not in group.
    """
    global _GROUP_CURRENT_NAME, _GROUP_START_TIME  # pylint: disable=global-statement
    if _GROUP_START_TIME is None:
        raise RuntimeError("Group not started")

    end_message = f"{_GROUP_CURRENT_NAME} completed in {time.time() - _GROUP_START_TIME:.3f} secs"
    log("INFO", end_message)

    if os.environ.get("GITHUB_ACTIONS"):
        separator = "::endgroup::"
    else:
        separator = "-" * (len(cast(str, _GROUP_CURRENT_NAME)) + 42)

    _GROUP_CURRENT_NAME = None
    _GROUP_START_TIME = None

    log("INFO", separator)
    print(separator)
