from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.ui.scenes.scene import Scene


def test_construction() -> None:
    assert Scene(MagicMock())
