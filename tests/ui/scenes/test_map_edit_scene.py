from typing import List
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.scenes.map_edit_scene import MapEditScene


def test_construction() -> None:
    q: List[Event] = []
    assert MapEditScene(MagicMock(), q.append)
