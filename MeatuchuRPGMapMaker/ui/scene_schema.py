from typing import Any

from schema import And, Optional, Schema

ELEMENT_SCHEMA = Schema(
    {
        "type": And(str, lambda x: x in ["root", "div", "text"]),
        Optional("children"): [And(dict[str, Any], lambda x: ELEMENT_SCHEMA.validate(x))],
    },
)

SCENE_SCHEMA = Schema(
    {
        "type": "root",
        "children": [lambda x: ELEMENT_SCHEMA.validate(x)],
    }
)

test = SCENE_SCHEMA.validate(
    {
        "type": "root",
        "children": [
            {
                "type": "div",
                "children": [
                    {"type": "text"},
                ],
            }
        ],
    }
)

print(test)
