"""Implementations for parsing the CLI arguments."""
import argparse
import os
from dataclasses import dataclass
from typing import cast

__all__ = ("CliArgs", "get_cli_args")


@dataclass
class CliArgs:
    """CLI arguments."""

    version_code: str
    iv: str
    key: str
    buffer: str
    config_path: str


def get_cli_args() -> CliArgs:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description="Downloads and pre-processes Dragalia Lost assets.")

    parser.add_argument("version", help="Manifest version code")
    parser.add_argument("-iv", "--iv", help="IV to decrypt the manifest asset", type=str)
    parser.add_argument("-key", "--key", help="Key to decrypt the manifest asset", type=str)
    parser.add_argument("-b", "--buffer", help="Buffer to decrypt the manifest asset", type=str)
    parser.add_argument("-c", "--config", help="Config file path to use", type=str)

    args = parser.parse_args()

    return CliArgs(
        version_code=cast(str, args.version),
        iv=cast(str, args.iv or os.environ["CRYPTO_IV"]),
        key=cast(str, args.key or os.environ["CRYPTO_KEY"]),
        buffer=cast(str, args.buffer or os.environ["CRYPTO_BUFFER"]),
        config_path=cast(str, args.config)
    )
