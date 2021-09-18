from dlasset.args import get_cli_args
from dlasset.config import load_config


def main():
    args = get_cli_args()
    config = load_config(args.config_path)

    print(config)


if __name__ == '__main__':
    main()
