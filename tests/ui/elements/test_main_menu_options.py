# pyright: reportPrivateUsage=false
from tkinter import Tk
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.ui.elements.composed_elements.main_menu.options_list import (
    MainMenuOptions,
)


def test_main_menu_options_can_be_constructed() -> None:
    window = Tk()
    main_menu_options = MainMenuOptions(window, lambda event: None)
    assert len(main_menu_options._elements)
    assert main_menu_options is not None


def test_main_menu_options_tick_update() -> None:
    window = Tk()
    main_menu_options = MainMenuOptions(window, lambda event: None)
    main_menu_options.tick_update()


def test_main_menu_options_frame_update() -> None:
    window = Tk()
    main_menu_options = MainMenuOptions(window, lambda event: None)
    main_menu_options.frame_update()


def test_main_menu_options_destroy() -> None:
    window = Tk()
    main_menu_options = MainMenuOptions(window, lambda event: None)
    for el in main_menu_options._elements.values():
        el.destroy = MagicMock()
    main_menu_options.destroy()
    for el in main_menu_options._elements.values():
        el.destroy.assert_called_once()  # pyright: ignore[reportFunctionMemberAccess]
