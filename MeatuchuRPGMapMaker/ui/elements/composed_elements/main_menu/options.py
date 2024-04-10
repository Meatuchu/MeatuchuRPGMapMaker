from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events.Event import Event
from MeatuchuRPGMapMaker.events.LogEvent import LogEvent
from MeatuchuRPGMapMaker.events.SceneChangeRequestEvent import SceneChangeRequestEvent

from ....elements.primitive_elements import Button
from .. import ComposedElement


class MainMenuOptions(ComposedElement):
    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        x: int = 0,
        y: int = 0,
        name: str = "mainmenuoptions",
    ) -> None:
        super().__init__(window, name, fire_event)

        self._elements = {
            "startbutton": StartButton(window, fire_event, x, y),
        }

    def tick_update(self) -> None:
        super().tick_update()


class StartButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None], x: int = 0, y: int = 0) -> None:
        def press_handler():
            fire_event(LogEvent("INFO", "Start button pressed", "MainMenuOptions_StartButton"))
            fire_event(LogEvent("INFO", f"{type(SceneChangeRequestEvent)}", "MainMenuOptions_StartButton"))
            fire_event(SceneChangeRequestEvent("MapEditScene"))

        super().__init__(
            window,
            fire_event,
            "startbutton",
            "Start",
            x=x + 5,
            y=y + 5,
            press_handler=press_handler,
        )
