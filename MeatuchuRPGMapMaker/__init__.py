import sys
from typing import List, Optional
import os

arguments: List[str] = sys.argv[1:]

parsed_args = {}


def process_args() -> None:
    val_name: Optional[str] = None
    for arg in arguments:
        if arg == "--":
            continue
        if arg.startswith("--"):
            if not val_name:
                val_name = arg
            else:
                continue
        elif arg.startswith("-"):
            if not val_name:
                parsed_args[arg] = True
            else:
                continue
        else:
            if val_name:
                parsed_args[val_name] = arg


process_args()
STAGE: str = parsed_args.get("--stage", "prod")  # type: ignore
ROOTDIR: str = os.path.dirname(__file__)
