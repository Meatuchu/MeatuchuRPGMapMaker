# pyright: reportPrivateUsage=false

from typing import List
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.scenes.map_edit_scene import MapEditScene


def test_construction() -> None:
    q: List[Event] = []
    assert MapEditScene(MagicMock(), "test", q.append)


def test_unload() -> None:
    q: List[Event] = []
    s = MapEditScene(MagicMock(), "test", q.append)
    s.unload()
    assert not s._subscription_ids
    assert not s._elements
