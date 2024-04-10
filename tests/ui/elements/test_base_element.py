# pyright: reportPrivateUsage=false
from typing import List
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.elements.primitive_elements.base_element import Element


def test_construction() -> None:
    q: List[Event] = []
    assert Element(MagicMock(), q.append, "testelement")


def test_fire_event() -> None:
    q: List[Event] = []
    event = Event()
    element = Element(MagicMock(), q.append, "testelement")
    element._fire_event(event)
    assert q == [event]
