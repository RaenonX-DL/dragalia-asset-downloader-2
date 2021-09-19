"""Workflows for processing the assets."""
from .config import load_config
from .env import Environment, get_cli_args, init_env
from .manifest import Manifest, decrypt_manifest_all_locale, download_manifest_all_locale, export_manifest_all_locale

__all__ = ("initialize", "process_manifest")


def initialize() -> Environment:
    """Initialize."""
    args = get_cli_args()
    config = load_config(args.config_path)

    env = init_env(args, config)
    env.print_info()

    return env


def process_manifest(env: Environment) -> Manifest:
    """Process manifest asset and return its model."""
    download_manifest_all_locale(env)
    decrypt_manifest_all_locale(env)
    return export_manifest_all_locale(env)
