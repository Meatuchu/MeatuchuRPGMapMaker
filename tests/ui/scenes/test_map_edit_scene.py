from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.ui.scenes.map_edit_scene import MapEditScene


def test_construction() -> None:
    assert MapEditScene(MagicMock())
