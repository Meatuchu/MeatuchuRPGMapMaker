from tkinter import Tk as TkWindow
from typing import Callable, Dict, List

from .....events.Event import Event
from ...primitive_elements import Button, Frame
from ...primitive_elements.base_element import Element, ElementPlacingMode
from .. import ComposedElement


class TabbedFrameTab:
    btn: Button
    frame: Frame
    frame_contents: List[Element]
    visible: bool = False

    def __init__(self, btn: Button, frame: Frame) -> None:
        self.btn = btn
        self.frame = frame
        self.frame_contents = []
        self.visible = False


class TabbedFrame(ComposedElement):
    tabs: Dict[str, TabbedFrameTab]
    active_tab: str

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
        self.active_tab = ""

    def add_tab(self, label: str, name: str) -> None:
        frame = Frame(
            self.window,
            self._fire_event,
            f"{self.name}_{name}frame",
            x=self.x,
            y=self.y,
            y_offset=25,
            width=300 + len(self.tabs) * 100,
            place_on_creation=False,
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
            press_handler=lambda: self.show_tab(name),
        )
        self._next_tab_offset += button_width
        self.add_element(frame)
        self.add_element(frame_btn)
        self.tabs[name] = TabbedFrameTab(frame_btn, frame)
        if not self.active_tab:
            self.show_tab(name)

    def add_element_to_tab(self, tab_name: str, element: Element) -> None:
        element_list = self.tabs[tab_name].frame_contents
        element_list.append(element)

        if self.tabs[tab_name].visible:
            element.place()

    def show_tab(self, tab_name: str) -> None:
        print(f"Showing tab: {tab_name}")
        self.hide_tab(self.active_tab)
        self.active_tab = tab_name
        for tab in self.tabs.values():
            tab.frame.hide()
            tab.visible = False

        tab = self.tabs[tab_name]
        tab.frame.place()
        tab.visible = True

        for element in tab.frame_contents:
            element.place()
        print(f"Active tab: {self.active_tab}")

    def hide_tab(self, tab_name: str) -> None:
        if not tab_name:
            return
        print(f"Hiding tab: {tab_name}")
        tab = self.tabs[tab_name]
        tab.frame.hide()
        tab.visible = False

        for element in tab.frame_contents:
            element.hide()

    def tick_update(self) -> None:
        super().tick_update()
