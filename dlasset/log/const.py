"""Constants about logging."""
from typing import Literal

__all__ = ("LogLevel", "LOG_LEVEL_NUM", "LOG_LEVEL_COLOR", "COLOR_RESET")

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

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
