"""Logging handlers."""
import logging
import os

__all__ = ("PIDFileHandler",)


def _file_path_with_pid(log_dir: str) -> str:
    pid = os.getpid()
    return os.path.join(log_dir, f"P-{pid}.log")


class PIDFileHandler(logging.FileHandler):
    """Logging handler to store the log of a certain PID."""

    def __init__(self, log_dir: str) -> None:
        file_path = _file_path_with_pid(log_dir)
        super().__init__(file_path)
