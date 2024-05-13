from tkinter import Tk as TkWindow
from typing import Callable, Dict, Literal, Union

from .....events.Event import Event
from ...primitive_elements import Button, Frame
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
    ) -> None:
        super().__init__(window, name, fire_event)
        self.x = x
        self.y = y
        self.tabs = {}

    def add_tab(self, label: str, name: str) -> None:
        frame = Frame(
            self.window,
            self._fire_event,
            f"{self.name}_{name}frame",
            x=self.x,
            y=self.y + 25,
        )
        frame_btn = Button(
            self.window,
            self._fire_event,
            f"{self.name}_{name}btn",
            label=label,
            height=25,
            width=(25 + (10 * len(label))),
            x=self.x,
            y=self.y,
            press_handler=frame.hide,
        )
        self.add_element(frame)
        self.add_element(frame_btn)
        self.tabs[name] = {"btn": frame_btn, "frame": frame}

    def tick_update(self) -> None:
        super().tick_update()
