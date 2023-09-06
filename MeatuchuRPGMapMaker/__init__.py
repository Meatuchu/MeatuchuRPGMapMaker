import sys

arguments = sys.argv[1:]


def set_stage() -> str:
    try:
        return arguments[0]
    except:
        return "prod"


STAGE = set_stage()
