from typing import Any

from schema import And, Optional, Schema

from .types import Margin, Padding

ELEMENT_SCHEMA = Schema(
    {
        "type": And(str, lambda x: x in ["root", "div", "text"]),
        Optional("children"): [And(dict[str, Any], lambda x: ELEMENT_SCHEMA.validate(x))],
        "text": str,
        Optional("id"): str,
        Optional("margin"): Margin,
        Optional("padding"): Padding,
    },
)

SCENE_SCHEMA = Schema(
    {
        "type": "root",
        "children": [lambda x: ELEMENT_SCHEMA.validate(x)],
    }
)
