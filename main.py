from dlasset.utils import time_exec
from dlasset.workflow import export_assets, initialize, process_manifest


@time_exec("Assets downloading & preprocessing")
def main():
    env = initialize()
    manifest = process_manifest(env)

    export_assets(env, manifest)


if __name__ == '__main__':
    main()
