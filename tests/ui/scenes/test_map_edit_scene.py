# pyright: reportPrivateUsage=false
from typing import Any
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.scene.scenes.map_edit_scene import MapEditScene


def test_construction() -> None:
    q: list[Event | dict[str, Any]] = []
    assert MapEditScene(MagicMock(), "test", q.append)


def test_unload() -> None:
    q: list[Event | dict[str, Any]] = []
    s = MapEditScene(MagicMock(), "test", q.append)
    s.unload()
    assert not s._subscription_ids
    assert not s._elements
