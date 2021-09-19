from dlasset.utils import time_exec
from dlasset.workflow import initialize, process_manifest


@time_exec("Assets downloading & preprocessing")
def main():
    env = initialize()
    process_manifest(env)


if __name__ == '__main__':
    main()
