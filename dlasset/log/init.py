"""Implementations for initializing the logging factory."""
import logging
import sys

from .middleware import PIDFileHandler

__all__ = ("init_log",)

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime}.{msecs:03.0f} PID-{process:>5} [{levelname:>8}]: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    stream=sys.stdout
)


def init_log(log_dir: str) -> None:
    """Configure the logging factory."""
    logging.getLogger().addHandler(PIDFileHandler(log_dir))
