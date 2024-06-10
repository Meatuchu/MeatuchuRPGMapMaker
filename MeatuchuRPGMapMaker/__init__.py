import os
import sys
from typing import Any

DEFAULT_STAGE: str = "prod"


arguments: list[str] = sys.argv[1:]
parsed_args: dict[str, str | bool] = {}


def process_args() -> None:
    key: str | None = None
    for arg in arguments:
        if not key:
            if arg.startswith("---") or not arg.startswith("-"):
                raise ValueError(f'Error parsing arguments: unexpected symbol "{arg}"')

        if arg == "--":
            continue

        if arg.startswith("-"):
            parsed_args[arg] = True
            if not key:
                key = arg
                continue

        if key:
            parsed_args[key] = arg
            key = None


def get_arg_value(key: str) -> Any:
    if key.startswith("-"):
        return parsed_args.get(key, None)
    else:
        KeyError("Arguments must start with one or two dashes!")


def set_arg_value(key: str) -> None:
    if not key.startswith("-") or key.startswith("---"):
        raise KeyError("Arguments must start with one or two dashes!")


process_args()


def get_all_args() -> dict[str, str | bool]:
    return parsed_args


STAGE_STR: str = get_arg_value("-s") or get_arg_value("--stage") or "prod"
VERBOSE_FLAG: bool = get_arg_value("-v") or get_arg_value("--verbose") or False
ROOTDIR: str = os.path.dirname(__file__)
