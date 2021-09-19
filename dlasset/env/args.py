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
    config_path: str
    no_index: bool


def get_cli_args() -> CliArgs:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description="Downloads and pre-processes Dragalia Lost assets.")

    parser.add_argument("version", type=str,
                        help="Manifest version code")
    parser.add_argument("-iv", "--iv", type=str,
                        help="IV to decrypt the manifest asset")
    parser.add_argument("-key", "--key", type=str,
                        help="Key to decrypt the manifest asset")
    parser.add_argument("-c", "--config", type=str,
                        help="Config file path to use")
    parser.add_argument("-ni", "--no-index", action="store_true", default=False,
                        help="File index will be ignored if this flag is provided")

    args = parser.parse_args()

    return CliArgs(
        version_code=cast(str, args.version),
        iv=cast(str, args.iv or os.environ["CRYPTO_IV"]),
        key=cast(str, args.key or os.environ["CRYPTO_KEY"]),
        config_path=cast(str, args.config),
        no_index=cast(bool, args.no_index),
    )
