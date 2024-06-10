from tkinter import Tk as TkWindow
from typing import Callable

from .....events.Event import Event
from ...primitive_elements import Button, Frame
from ...primitive_elements.base_element import (
    Element,
    ElementPlacingMode,
    ElementSizingMode,
)
from .. import ComposedElement


class TabbedFrameTab:
    btn: Button
    frame: Frame
    frame_contents: list[Element]
    visible: bool = False

    def __init__(self, btn: Button, frame: Frame) -> None:
        self.btn = btn
        self.frame = frame
        self.frame_contents = []
        self.visible = False


class TabbedFrame(ComposedElement):
    tabs: dict[str, TabbedFrameTab]
    active_tab: str
    TAB_HEIGHT: int = 25

    def __init__(
        self,
        window: TkWindow,
        name: str,
        fire_event: Callable[[Event], None],
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        width: int = 100,
        height: int = 100,
        height_offset: int = 0,
        width_offset: int = 0,
        sizing_mode: ElementSizingMode = "absolute",
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        super().__init__(window, name, fire_event, sizing_mode=sizing_mode, placing_mode=placing_mode)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.height_offset = height_offset
        self.width_offset = width_offset
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
            x=self.x + self.x_offset,
            y=self.y + self.y_offset,
            y_offset=self.TAB_HEIGHT,
            width=self.width,
            height=self.height,
            height_offset=(-1 * self.TAB_HEIGHT) + self.height_offset,
            width_offset=self.width_offset,
            place_on_creation=False,
            sizing_mode=self.sizing_mode,
        )
        button_width = 25 + (7 * len(label))
        frame_btn = Button(
            self.window,
            self._fire_event,
            f"{self.name}_{name}btn",
            label=label,
            height=self.TAB_HEIGHT,
            width=button_width,
            x=self.x + self.x_offset,
            x_offset=self._next_tab_offset,
            y=self.y + self.y_offset,
            press_handler=lambda: self.show_tab(name),
        )
        self._next_tab_offset += button_width
        self.add_element(frame)
        self.add_element(frame_btn)
        self.tabs[name] = TabbedFrameTab(frame_btn, frame)
        if not self.active_tab:
            self.show_tab(name)

    def add_element_to_tab(self, tab_name: str, element: Element, frame_posx: int = 0, frame_posy: int = 0) -> None:
        self.add_element(element)
        frame = self.tabs[tab_name].frame
        frame_element_list = self.tabs[tab_name].frame_contents
        frame_element_list.append(element)
        element.move_to(
            frame_posx + self.x + frame.frame_bordersize, frame_posy + self.y + frame.frame_bordersize + self.TAB_HEIGHT
        )

        if self.tabs[tab_name].visible:
            element.place()

    def show_tab(self, tab_name: str) -> None:
        if self.active_tab == tab_name:
            return
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

    def hide_tab(self, tab_name: str) -> None:
        if not tab_name:
            return
        tab = self.tabs[tab_name]
        tab.frame.hide()
        tab.visible = False

        for element in tab.frame_contents:
            element.hide()

    def tick_update(self) -> None:
        super().tick_update()

    def handle_window_resize(self) -> None:
        self.tabs[self.active_tab].btn.handle_window_resize()
        self.tabs[self.active_tab].frame.handle_window_resize()
        for e in self.tabs[self.active_tab].frame_contents:
            e.handle_window_resize()
        return super().handle_window_resize()
