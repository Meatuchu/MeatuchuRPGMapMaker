# pyright: reportPrivateUsage=false
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event, EventQueueItemType
from MeatuchuRPGMapMaker.ui.elements.primitive_elements.base_element import Element


def test_construction() -> None:
    q: list[EventQueueItemType] = []
    assert Element(MagicMock(), q.append, "testelement")


def test_fire_event() -> None:
    q: list[EventQueueItemType] = []
    event = Event()
    element = Element(MagicMock(), q.append, "testelement")
    element._fire_event(event)
    assert q == [event]


def test_hide() -> None:
    q: list[EventQueueItemType] = []
    element = Element(MagicMock(), q.append, "testelement")
    element.hide()
    assert not element.visible


def test_place() -> None:
    q: list[EventQueueItemType] = []
    element = Element(MagicMock(), q.append, "testelement")
    element.place()
    assert element.visible


def test_destroy() -> None:
    q: list[EventQueueItemType] = []
    element = Element(MagicMock(), q.append, "testelement")
    element.destroy()
    assert not element.visible
    assert element.destroyed
