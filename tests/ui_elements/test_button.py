from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.ui_elements.button import Button


def test_construction() -> None:
    assert Button()


def test_set_press_handler() -> None:
    button = Button()
    button.set_press_handler(MagicMock())


def test_press_handler() -> None:
    button = Button()
    h = MagicMock()
    button.set_press_handler(h)
    button.press_handler()
    h.assert_called_once()
