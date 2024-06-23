# pyright: reportPrivateUsage=false
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import EventQueueItemType
from MeatuchuRPGMapMaker.ui.scene.scenes.map_edit_scene import MapEditScene


def test_construction() -> None:
    q: list[EventQueueItemType] = []
    MapEditScene.inject_queue_event(q.append)
    assert MapEditScene(MagicMock(), "test")


def test_unload() -> None:
    q: list[EventQueueItemType] = []
    MapEditScene.inject_queue_event(q.append)
    s = MapEditScene(MagicMock(), "test")
    s.unload()
    assert not s._subscription_ids
    assert not s._elements
