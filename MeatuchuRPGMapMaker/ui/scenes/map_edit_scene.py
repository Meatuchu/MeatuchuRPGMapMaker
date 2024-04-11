from tkinter import Tk as TkWindow
from typing import Callable, Optional, Type

from MeatuchuRPGMapMaker.events import LogEvent, SceneChangeRequestEvent

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


class MainMenuButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        def press_handler() -> None:
            fire_event(LogEvent("INFO", "Main menu button pressed", "MapEditScene_MainMenuButton"))
            fire_event(SceneChangeRequestEvent("MenuScene"))

        super().__init__(
            window,
            fire_event,
            "mainmenubutton",
            "Return to Main Menu",
            x=55,
            y=105,
            height=30,
            width=160,
            press_handler=press_handler,
        )
