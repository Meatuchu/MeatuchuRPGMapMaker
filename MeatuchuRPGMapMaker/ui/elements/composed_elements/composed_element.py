from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import Event, LogEvent

from ..primitive_elements.base_element import (
    Element,
    ElementPlacingMode,
    ElementSizingMode,
)


class ComposedElement(Element):
    # Composed Elements are elements treated as a single element, but which are comprised of one or more element classes
    # They are defined in their own folder to reduce the possibility of circular dependency.

    _elements: dict[str, Element]

    def __init__(
        self,
        window: TkWindow,
        name: str,
        fire_event: Callable[[Event], None],
        placing_mode: ElementPlacingMode = "absolute",
        sizing_mode: ElementSizingMode = "absolute",
    ) -> None:
        self._elements = {}
        super().__init__(window, fire_event, name, placing_mode=placing_mode, sizing_mode=sizing_mode)

    def add_element(self, element: Element) -> None:
        if self._elements.get(element.name):
            raise ValueError(f"Element with name {element.name} already exists in {self.name}")
        self._elements[element.name] = element

    def get_element(self, name: str) -> Element | None:
        res = self._elements.get(name)
        if not res:
            self._fire_event(
                LogEvent("WARNING", f"Failed to look up element {name} in ComposedElement {self.name}", self.name)
            )
        return res

    def tick_update(self) -> None:
        super().tick_update()
        for e in self._elements.values():
            e.tick_update()

    def frame_update(self) -> None:
        super().frame_update()
        for e in self._elements.values():
            e.frame_update()

    def hide(self) -> None:
        for e in self._elements.values():
            e.hide()
        return super().hide()

    def destroy(self) -> None:
        for e in self._elements.values():
            e.destroy()
        return super().destroy()

    def handle_window_resize(self) -> None:
        for e in self._elements.values():
            e.handle_window_resize()
        return super().handle_window_resize()
