from MeatuchuRPGMapMaker.ui.types import Margin, Padding

valid_scene_schema = {
    "type": "root",
    "children": [
        {"type": "text", "text": "test", "margin": Margin(0), "padding": Padding(0)},
    ],
}

duplicate_id_scene_schema = {
    "type": "root",
    "children": [
        {"id": "test", "type": "text", "text": "test", "margin": Margin(0), "padding": Padding(0)},
        {"id": "test", "type": "text", "text": "test", "margin": Margin(0), "padding": Padding(0)},
    ],
}

invalid_children_scene_schema = {
    "type": "root",
    "children": [
        {
            "type": "text",
            "text": "test",
            "margin": Margin(0),
            "padding": Padding(0),
            "children": [
                {"id": "test", "type": "text", "text": "test", "margin": Margin(0), "padding": Padding(0)},
            ],
        },
    ],
}
