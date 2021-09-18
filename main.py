from dlasset.args import get_cli_args
from dlasset.config import load_config
from dlasset.log import log


def main():
    args = get_cli_args()
    config = load_config(args.config_path)

    log("CRITICAL", config)
    log("ERROR", config)
    log("WARNING", config)
    log("INFO", config)
    log("DEBUG", config)


if __name__ == '__main__':
    main()
