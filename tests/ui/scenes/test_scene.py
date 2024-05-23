# pyright: reportPrivateUsage=false
from typing import Callable, Dict, List, Type
from unittest.mock import MagicMock
from uuid import uuid4

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.scenes.scene import Scene


def test_construction() -> None:
    q: List[Event] = []
    assert Scene(MagicMock(), "test", q.append)


def test_scene_subscribe_to_event() -> None:
    q: List[Event] = []
    subscriptions: Dict[str, Callable[[Event], None]] = {}

    mock_event_subfn = MagicMock()

    def subscribe_to_event(event: Type[Event], fn: Callable[[Event], None]) -> str:
        k = str(uuid4())
        subscriptions[k] = fn
        return k

    def unsubscribe_from_event(id: str) -> None:
        subscriptions.pop(id, None)

    s = Scene(MagicMock(), "test", q.append, subscribe_to_event, unsubscribe_from_event)
    subscriptions = {}  # clear out default subscriptions

    assert s._subscribe_to_event

    s._subscribe(Event, mock_event_subfn)
    s._subscribe(Event, mock_event_subfn)
    s._subscribe(Event, mock_event_subfn)
    assert len(subscriptions) == 3


def test_scene_unsubscribe_to_event() -> None:
    q: List[Event] = []
    subscriptions: Dict[str, Callable[[Event], None]] = {}

    mock_event_subfn = MagicMock()

    def subscribe_to_event(event: Type[Event], fn: Callable[[Event], None]) -> str:
        k = str(uuid4())
        subscriptions[k] = fn
        return k

    def unsubscribe_from_event(id: str) -> None:
        subscriptions.pop(id, None)

    s = Scene(MagicMock(), "test", q.append, subscribe_to_event, unsubscribe_from_event)
    subscriptions = {}  # clear out default subscriptions

    assert s._subscribe_to_event

    s._subscribe(Event, mock_event_subfn)
    s._subscribe(Event, mock_event_subfn)
    s._subscribe(Event, mock_event_subfn)
    assert len(subscriptions) == 3
    # assert not subscriptions
    s.unload()
    assert not subscriptions
