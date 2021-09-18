"""Implementations for parsing the CLI arguments."""
import argparse
from dataclasses import dataclass

__all__ = ("get_cli_args", "CliArgs")

from typing import cast


@dataclass
class CliArgs:
    """CLI arguments."""

    version_code: str
    iv: str
    key: str
    config_path: str


def get_cli_args() -> CliArgs:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description="Downloads and pre-processes Dragalia Lost assets.")

    parser.add_argument("version", help="Manifest version code")
    parser.add_argument("-iv", "--iv", help="IV to decrypt the manifest file", type=str, required=True)
    parser.add_argument("-key", "--key", help="Key to decrypt the manifest file", type=str, required=True)
    parser.add_argument("-c", "--config", help="Config file path to use", type=str, required=True)

    args = parser.parse_args()

    return CliArgs(
        version_code=cast(str, args.version),
        iv=cast(str, args.iv), key=cast(str, args.key),
        config_path=cast(str, args.config)
    )
