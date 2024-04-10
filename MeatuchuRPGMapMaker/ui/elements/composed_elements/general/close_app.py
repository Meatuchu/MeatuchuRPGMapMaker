from tkinter import Tk as TkWindow
from typing import Callable

from .....events.AppShutDownEvent import AppShutDownEvent
from .....events.Event import Event
from ....elements.primitive_elements import Button
from .. import ComposedElement


class CloseApp(ComposedElement):
    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        x: int = 0,
        y: int = 0,
        name: str = "closeapp",
    ) -> None:
        super().__init__(window, name, fire_event)

        self._elements = {
            "closeapp_btn": Button(
                window,
                fire_event,
                "closeapp_btn",
                "Close App",
                x=x,
                y=y,
                press_handler=lambda: fire_event(AppShutDownEvent()),
            ),
        }

    def tick_update(self) -> None:
        super().tick_update()
