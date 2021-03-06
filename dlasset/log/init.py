"""Implementations for initializing the logging factory."""
import logging
import os.path
import sys

from .const import LOGGER_CONSOLE
from .middleware import PIDFileHandler

__all__ = ("init_log",)

logging.basicConfig(
    level=logging.DEBUG,  # Root level needs to be lower than the subloggers
    handlers=[logging.NullHandler()]  # Don't output things
)

FORMAT = "{asctime}.{msecs:03.0f} PID-{process:>5} [{levelname:>8}]: {message}"
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

default_formatter = logging.Formatter(FORMAT, style="{", datefmt=FORMAT_DATE)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(default_formatter)

LOGGER_CONSOLE.addHandler(console_handler)


def init_log(log_dir: str) -> None:
    """Configure the logging factory."""
    pid_handler = PIDFileHandler(log_dir)
    pid_handler.setLevel(logging.DEBUG)
    pid_handler.setFormatter(default_formatter)

    # Log everything to PID log file
    logging.getLogger().addHandler(pid_handler)

    # Log error to a specific file
    file_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(default_formatter)

    # Log error to the specific file
    logging.getLogger().addHandler(file_handler)
