from MeatuchuRPGMapMaker.ui.scene_schema import SCENE_SCHEMA
from MeatuchuRPGMapMaker.ui.scenes import main_menu_scene_schema


def test_main_menu_scene() -> None:
    assert SCENE_SCHEMA.validate(main_menu_scene_schema)
