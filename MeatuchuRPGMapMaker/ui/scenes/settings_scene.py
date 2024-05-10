from tkinter import Tk as TkWindow
from typing import Callable, Optional, Type

from MeatuchuRPGMapMaker.events import LogEvent, SceneChangeRequestEvent

from ...events.Event import Event
from ..elements.primitive_elements import Button
from .scene import Scene


class SettingsScene(Scene):
    # Scene describes the UI when editing settings
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
            fire_event(LogEvent("DEBUG", "Main menu button pressed", "SettingsScene_MainMenuButton"))
            fire_event(SceneChangeRequestEvent("MenuScene"))

        super().__init__(
            window,
            fire_event,
            "mainmenubutton",
            "Return to Main Menu From Settings",
            x=15,
            y=15,
            height=30,
            width=250,
            press_handler=press_handler,
        )
