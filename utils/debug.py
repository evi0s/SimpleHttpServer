"""Debug"""
import config


def debug(message):
    if config.debug:
        print("\033[0;33;40m[Debug]\033[0m: %s" % message)
    else:
        pass


def error(message):
    print("\033[0;31;40m[Error]\033[0m: %s" % message)

