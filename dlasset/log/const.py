"""Constants about logging."""
import logging
from typing import Literal

__all__ = (
    "LogLevel", "LOG_LEVEL_NUM", "LOG_LEVEL_COLOR", "COLOR_RESET",
    "LOGGER_CONSOLE", "LOGGER_FILE", "LOGGER_ERROR"
)

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LOGGER_CONSOLE = logging.getLogger("console")
LOGGER_CONSOLE.propagate = False  # Console message will have ANSI colors, which is not desired for files

LOGGER_FILE = logging.getLogger("file")
LOGGER_FILE.propagate = True

LOGGER_ERROR = logging.getLogger("error")
LOGGER_ERROR.propagate = True

LOG_LEVEL_NUM: dict[LogLevel, int] = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}

LOG_LEVEL_COLOR: dict[LogLevel, str] = {
    "CRITICAL": "\x1b[35m",
    "ERROR": "\x1b[31m",
    "WARNING": "\x1b[33m",
    "INFO": "\x1b[36m",
    "DEBUG": "\x1b[37m",
}

COLOR_RESET: str = "\x1b[0m"
