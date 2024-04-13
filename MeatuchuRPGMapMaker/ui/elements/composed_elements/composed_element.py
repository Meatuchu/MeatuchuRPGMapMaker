from tkinter import Tk as TkWindow
from typing import Callable, Dict

from MeatuchuRPGMapMaker.events import Event

from ..primitive_elements.base_element import Element


class ComposedElement(Element):
    # Composed Elements are elements treated as a single element, but which are comprised of one or more element classes
    # They are defined in their own folder to reduce the possibility of circular dependency.

    _elements: Dict[str, Element]

    def __init__(self, window: TkWindow, name: str, fire_event: Callable[[Event], None]) -> None:
        super().__init__(window, fire_event, name)

    def add_element(self, element: Element) -> None:
        if self._elements.get(element.name):
            raise ValueError(f"Element with name {element.name} already exists in {self.name}")
        self._elements[element.name] = element

    def tick_update(self) -> None:
        super().tick_update()
        for e in self._elements.values():
            e.tick_update()

    def frame_update(self) -> None:
        super().frame_update()
        for e in self._elements.values():
            e.frame_update()

    def destroy(self) -> None:
        for e in self._elements.values():
            e.destroy()
        return super().destroy()
