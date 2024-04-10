from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import LogEvent, SceneChangeRequestEvent

from ...events.Event import Event
from ..elements.primitive_elements import Button
from .scene import Scene


class MapEditScene(Scene):
    # Primary scene of this app.
    # Scene describes the UI when creating and editing a map
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        super().__init__(window, fire_event)

        self.place_elements(
            [
                MainMenuButton(window, fire_event),
            ]
        )


class MainMenuButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        def press_handler():
            fire_event(LogEvent("INFO", "Main menu button pressed", "MapEditScene_MainMenuButton"))
            fire_event(SceneChangeRequestEvent("MenuScene"))

        super().__init__(
            window,
            fire_event,
            "mainmenubutton",
            "Return to Main Menu",
            x=100,
            y=200,
            press_handler=press_handler,
        )
