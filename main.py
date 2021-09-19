import time
from functools import wraps

from dlasset.args import get_cli_args
from dlasset.config import load_config
from dlasset.env import init_env
from dlasset.manifest import decrypt_manifest_all_locale, download_manifest_all_locale, export_manifest_all_locale


def time_exec(title: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _start = time.time()
            ret = fn(*args, **kwargs)
            print(f"{title} completed in {time.time() - _start:.3f} secs")
            return ret

        return wrapper

    return decorator


@time_exec("Assets downloading & preprocessing")
def main():
    args = get_cli_args()
    config = load_config(args.config_path)

    env = init_env(args, config)
    env.print_info()

    download_manifest_all_locale(env)
    decrypt_manifest_all_locale(env)
    export_manifest_all_locale(env)


if __name__ == '__main__':
    main()
