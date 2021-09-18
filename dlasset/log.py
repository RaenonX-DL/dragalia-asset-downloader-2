"""Implementations for logging."""
import logging
import os
import sys
import time
from typing import Any, Literal, Optional, cast, no_type_check

__all__ = ("log", "log_group_start", "log_group_end")

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

_LOG_LEVEL_NUM: dict[LogLevel, int] = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}

_LOG_LEVEL_COLOR: dict[LogLevel, str] = {
    "CRITICAL": "\x1b[35m",
    "ERROR": "\x1b[31m",
    "WARNING": "\x1b[33m",
    "INFO": "\x1b[36m",
    "DEBUG": "\x1b[37m",
}

_COLOR_RESET: str = "\x1b[0m"

_GROUP_START_TIME: Optional[float] = None
_GROUP_CURRENT_NAME: Optional[str] = None

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime}.{msecs:.0f} [{levelname:>8}]: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    stream=sys.stdout,
)


@no_type_check
def log(level: LogLevel, message: Any) -> None:
    """Log ``message`` at ``level``."""
    logging.log(_LOG_LEVEL_NUM[level], _LOG_LEVEL_COLOR[level], message, _COLOR_RESET)


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
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::group::{name}")
    else:
        print(f"{'-' * 20} {name} {'-' * 20}")


def log_group_end() -> None:
    """
    Place a group end marker.

    Raises :class:`RuntimeError` if currently not in group.
    """
    global _GROUP_CURRENT_NAME, _GROUP_START_TIME  # pylint: disable=global-statement
    if _GROUP_START_TIME is None:
        raise RuntimeError("Group not started")

    print(f"{_GROUP_CURRENT_NAME} completed in {time.time() - _GROUP_START_TIME:.3f} secs")
    if os.environ.get("GITHUB_ACTIONS"):
        print("::endgroup::")
    else:
        print("-" * (len(cast(str, _GROUP_CURRENT_NAME)) + 42))
    _GROUP_CURRENT_NAME = None
    _GROUP_START_TIME = None
