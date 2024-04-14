from tkinter import Tk as TkWindow
from typing import Callable, Optional, Type

from MeatuchuRPGMapMaker.events import LogEvent, SceneChangeRequestEvent
from MeatuchuRPGMapMaker.keybinds.common.file_save import FileSaveKB

from ...events.Event import Event
from ..elements.primitive_elements import Button
from .scene import Scene


class MapEditScene(Scene):
    # Primary scene of this app.
    # Scene describes the UI when creating and editing a map
    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        subscribe_to_event: Optional[Callable[[Type[Event], Callable[..., None]], str]] = None,
        unsubscribe_from_event: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__(window, fire_event, subscribe_to_event, unsubscribe_from_event)

        self.place_elements(
            [
                MainMenuButton(window, fire_event),
            ]
        )
        self._add_keybind(FileSaveKB(self._fire_event))


class MainMenuButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        def press_handler() -> None:
            fire_event(LogEvent("DEBUG", "Main menu button pressed", "MapEditScene_MainMenuButton"))
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
