"""Workflows for processing the assets."""
from .config import load_config
from .env import Environment, get_cli_args, init_env
from .export import export_by_task, export_raw_by_task
from .manifest import Manifest, decrypt_manifest_all_locale, download_manifest_all_locale, export_manifest_all_locale

__all__ = ("initialize", "process_manifest", "export_assets")


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


def export_assets(env: Environment, manifest: Manifest) -> None:
    """Perform asset exporting tasks in the config."""
    for asset_task in env.config.asset_tasks:
        export_by_task(env, manifest, asset_task)

        # Update index file per task
        env.index.update_index_files()

    for raw_task in env.config.raw_tasks:
        export_raw_by_task(env, manifest, raw_task)
