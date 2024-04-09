from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.ui.elements.primitive_elements import Button


def test_construction() -> None:
    assert Button(MagicMock(), "testbutton")


def test_set_press_handler() -> None:
    button = Button(MagicMock(), "testbutton")
    button.set_press_handler(MagicMock())


def test_press_handler() -> None:
    button = Button(MagicMock(), "testbutton")
    h = MagicMock()
    button.set_press_handler(h)
    button.press_handler()
    h.assert_called_once()
