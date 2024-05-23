# pyright: reportPrivateUsage=false
from typing import List
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.elements.primitive_elements import Button


def test_construction() -> None:
    q: List[Event] = []
    assert Button(MagicMock(), q.append, "testbutton")


def test_set_press_handler() -> None:
    q: List[Event] = []
    button = Button(MagicMock(), q.append, "testbutton")
    button.set_press_handler(MagicMock())


def test_press_handler() -> None:
    q: List[Event] = []
    button = Button(MagicMock(), q.append, "testbutton")
    h = MagicMock()
    button.set_press_handler(h)
    button.press_handler()
    h.assert_called_once()


def test_destroy() -> None:
    q: List[Event] = []
    button = Button(MagicMock(), q.append, "testbutton")
    button._tkinter_button = MagicMock()
    button.destroy()
    button._tkinter_button.destroy.assert_called_once()
    assert not button.visible
    assert button.destroyed


def test_hide() -> None:
    q: List[Event] = []
    button = Button(MagicMock(), q.append, "testbutton")
    button._tkinter_button = MagicMock()
    button.hide()
    button._tkinter_button.place_forget.assert_called_once()
    assert not button.visible
