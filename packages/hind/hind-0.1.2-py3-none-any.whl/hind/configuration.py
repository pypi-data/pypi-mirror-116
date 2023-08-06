from os.path import expanduser

from yaml import FullLoader, dump, load


def read_configuration():
    home = expanduser("~")

    with open(f"{home}/.hind", "rt") as handle:
        return load(handle.read(), Loader=FullLoader)


def write_configuration(configuration):
    home = expanduser("~")

    with open(f"{home}/.hind", "wt") as handle:
        handle.write(dump(configuration))
