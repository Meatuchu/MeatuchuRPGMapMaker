from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import (
    Event,
    SceneChangeRequestEvent,
)
from MeatuchuRPGMapMaker.keybinds.common.file_save import FileSaveKB

from ...elements.primitive_elements import Button
from ..scene import Scene


class MapEditScene(Scene):
    # Primary scene of this app.
    # Scene describes the UI when creating and editing a map
    def __init__(
        self,
        window: TkWindow,
        window_name: str,
    ) -> None:
        super().__init__(window, window_name)

        self.place_elements(
            [
                MainMenuButton(window, self.fire_event),
            ]
        )
        self.add_keybind(FileSaveKB(self.fire_event))


class MainMenuButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        def press_handler() -> None:
            fire_event(SceneChangeRequestEvent("MenuScene"))

        super().__init__(
            window,
            fire_event,
            "mainmenubutton",
            "Return to Main Menu",
            x=15,
            y=15,
            height=30,
            width=160,
            press_handler=press_handler,
        )
