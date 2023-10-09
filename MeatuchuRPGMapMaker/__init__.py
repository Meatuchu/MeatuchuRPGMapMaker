import sys
from typing import List, Optional, Any
import os

arguments: List[str] = sys.argv[1:]

parsed_args = {}


def process_args() -> None:
    val_name: Optional[str] = None
    for arg in arguments:
        if arg.startswith("---") and not val_name:
            raise KeyError(f"Arguments must start with one or two dashes!")
        if arg == "--":
            continue
        if arg.startswith("--"):
            val_name = arg
            continue
        if arg.startswith("-"):
            if not val_name:
                parsed_args[arg] = True
            else:
                val_name = None
                continue

        if val_name:
            parsed_args[val_name] = arg


def get_arg_value(key: str) -> Optional[Any]:
    if key.startswith("--"):
        return parsed_args.get(key, None)  # type: ignore
    elif key.startswith("-"):
        if parsed_args.get(key):
            return True
        else:
            return False
    else:
        KeyError("Arguments must start with one or two dashes!")


def set_arg_value(key: str) -> None:
    if not key.startswith("-") or key.startswith("---"):
        raise KeyError("Arguments must start with one or two dashes!")


process_args()

STAGE_STR: str = get_arg_value("--stage") or "prod"
ROOTDIR: str = os.path.dirname(__file__)
