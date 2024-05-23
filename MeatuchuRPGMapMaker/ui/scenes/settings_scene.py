from tkinter import Tk as TkWindow
from typing import Callable, Optional, Type

from MeatuchuRPGMapMaker.events import LogEvent, SceneChangeRequestEvent

from ...events.Event import Event
from ..elements.composed_elements.general.tabbed_frame import TabbedFrame
from ..elements.primitive_elements import Button
from .scene import Scene


class SettingsScene(Scene):
    # Scene describes the UI when editing settings
    def __init__(
        self,
        window: TkWindow,
        window_name: str,
        fire_event: Callable[[Event], None],
        subscribe_to_event: Optional[Callable[[Type[Event], Callable[..., None]], str]] = None,
        unsubscribe_from_event: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__(window, window_name, fire_event, subscribe_to_event, unsubscribe_from_event)

        self._frames = TabbedFrame(window, "SettingsSceneTabbedFrame", fire_event)

        self.place_elements(
            [
                MainMenuButton(window, fire_event),
                self._frames,
            ]
        )
        self._frames.add_tab("test", "test")
        self._frames.add_tab("test2", "test2")
        self._frames.add_tab("test3 with a really dang long name", "test3")


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
            y=400,
            height=30,
            width=250,
            press_handler=press_handler,
        )
