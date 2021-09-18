import asyncio

from dlasset.args import get_cli_args
from dlasset.config import load_config
from dlasset.env import download_manifest_all_locale, init_env
from dlasset.log import log, log_group_end, log_group_start


def print_config(env):
    log_group_start("Environment config")
    log("INFO", f"Manifest asset directory: {env.manifest_asset_dir}")
    log("INFO", f"Downloaded assets directory: {env.assets_dir}")
    log_group_end()


async def main():
    args = get_cli_args()
    config = load_config(args.config_path)

    env = init_env(args, config)
    print_config(env)

    await download_manifest_all_locale(env)


if __name__ == '__main__':
    # https://stackoverflow.com/a/66772242/11571888
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
