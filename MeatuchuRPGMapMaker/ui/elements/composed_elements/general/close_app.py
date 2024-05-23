from tkinter import Tk as TkWindow
from typing import Callable

from .....events.AppShutDownEvent import AppShutDownEvent
from .....events.Event import Event
from ...primitive_elements import Button
from ...primitive_elements.base_element import ElementPlacingMode
from .. import ComposedElement


class CloseAppButton(ComposedElement):
    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        x: int = 0,
        y: int = 0,
        name: str = "closeapp",
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        super().__init__(window, name, fire_event, placing_mode=placing_mode)

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
