"""Implementations for logging."""
import logging
import sys
from typing import Any, Literal, no_type_check

__all__ = ("log",)

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

_log_level_num: dict[LogLevel, int] = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}

_log_level_color: dict[LogLevel, str] = {
    "CRITICAL": "\x1b[35m",
    "ERROR": "\x1b[31m",
    "WARNING": "\x1b[33m",
    "INFO": "\x1b[36m",
    "DEBUG": "\x1b[37m",
}

_color_reset: str = "\x1b[0m"

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime}.{msecs:.0f} [{levelname:>8}]: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    stream=sys.stdout,
)


@no_type_check
def log(level: LogLevel, message: Any):
    """Log ``message`` at ``level``."""
    logging.log(_log_level_num[level], f"{_log_level_color[level]}{message}{_color_reset}")
