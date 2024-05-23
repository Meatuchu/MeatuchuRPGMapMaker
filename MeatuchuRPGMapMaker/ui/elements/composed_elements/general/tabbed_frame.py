from tkinter import Tk as TkWindow
from typing import Callable, Dict, Literal, Union

from .....events.Event import Event
from ...primitive_elements import Button, Frame
from ...primitive_elements.base_element import ElementPlacingMode
from .. import ComposedElement


class TabbedFrame(ComposedElement):
    tabs: Dict[str, Dict[Literal["btn", "frame"], Union[Button, Frame]]]

    def __init__(
        self,
        window: TkWindow,
        name: str,
        fire_event: Callable[[Event], None],
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        super().__init__(window, name, fire_event, placing_mode=placing_mode)
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self._next_tab_offset = 0
        self.tabs = {}

    def add_tab(self, label: str, name: str) -> None:
        frame = Frame(
            self.window,
            self._fire_event,
            f"{self.name}_{name}frame",
            x=self.x,
            y=self.y,
            y_offset=25,
        )
        button_width = 25 + (7 * len(label))
        frame_btn = Button(
            self.window,
            self._fire_event,
            f"{self.name}_{name}btn",
            label=label,
            height=25,
            width=button_width,
            x=self.x,
            x_offset=self._next_tab_offset,
            y=self.y,
            press_handler=frame.hide,
        )
        self._next_tab_offset += button_width
        self.add_element(frame)
        self.add_element(frame_btn)
        self.tabs[name] = {"btn": frame_btn, "frame": frame}

    def tick_update(self) -> None:
        super().tick_update()
