from tkinter import Tk as TkWindow
from typing import Callable

from .....events.Event import Event
from .....events.LogEvent import LogEvent
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
            "startbutton": Button(
                window,
                fire_event,
                "startbutton",
                "Start",
                x=x + 5,
                y=y + 5,
                press_handler=lambda: fire_event(
                    LogEvent("INFO", "Start button pressed", "MainMenuOptions_StartButton")
                ),
            ),
        }

    def tick_update(self) -> None:
        super().tick_update()
