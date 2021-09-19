from dlasset.utils import time_exec
from dlasset.workflow import initialize, process_manifest


@time_exec("Assets downloading & preprocessing")
def main():
    env = initialize()
    manifest = process_manifest(env)

    print(manifest)


if __name__ == '__main__':
    main()
