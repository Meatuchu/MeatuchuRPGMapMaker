# pyright: reportPrivateUsage=false
from typing import Callable, Type
from unittest.mock import MagicMock
from uuid import uuid4

from MeatuchuRPGMapMaker.events import Event, EventQueueItemType
from MeatuchuRPGMapMaker.ui.scene.scene import Scene


def test_construction() -> None:
    q: list[EventQueueItemType] = []
    Scene.inject_queue_event(q.append)
    assert Scene(MagicMock(), "test")


def test_scene_subscribe_to_event() -> None:
    q: list[EventQueueItemType] = []
    subscriptions: dict[str, Callable[[Event], None]] = {}

    mock_event_subfn = MagicMock()

    def subscribe_to_event(event: Type[Event], fn: Callable[[Event], None]) -> str:
        k = str(uuid4())
        subscriptions[k] = fn
        return k

    def unsubscribe_from_event(id: str) -> None:
        subscriptions.pop(id, None)

    Scene.inject_subscribe_to_event(subscribe_to_event)
    Scene.inject_unsubscribe_from_event(unsubscribe_from_event)
    Scene.inject_queue_event(q.append)
    s = Scene(MagicMock(), "test")
    subscriptions = {}  # clear out default subscriptions

    assert s._subscribe_to_event

    s.subscribe(Event, mock_event_subfn)
    s.subscribe(Event, mock_event_subfn)
    s.subscribe(Event, mock_event_subfn)
    assert len(subscriptions) == 3


def test_scene_unsubscribe_to_event() -> None:
    q: list[EventQueueItemType] = []
    subscriptions: dict[str, Callable[[Event], None]] = {}

    mock_event_subfn = MagicMock()

    def subscribe_to_event(event: Type[Event], fn: Callable[[Event], None]) -> str:
        k = str(uuid4())
        subscriptions[k] = fn
        return k

    def unsubscribe_from_event(id: str) -> None:
        subscriptions.pop(id, None)

    Scene.inject_subscribe_to_event(subscribe_to_event)
    Scene.inject_unsubscribe_from_event(unsubscribe_from_event)
    Scene.inject_queue_event(q.append)

    s = Scene(MagicMock(), "test")
    subscriptions = {}  # clear out default subscriptions

    assert s._subscribe_to_event

    s.subscribe(Event, mock_event_subfn)
    s.subscribe(Event, mock_event_subfn)
    s.subscribe(Event, mock_event_subfn)
    assert len(subscriptions) == 3
    # assert not subscriptions
    s.unload()
    assert not subscriptions
