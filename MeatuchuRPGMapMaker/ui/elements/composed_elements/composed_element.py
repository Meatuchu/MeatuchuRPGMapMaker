from typing import Dict
from tkinter import Tk as TkWindow
from ..primitive_elements.base_element import Element


class ComposedElement(Element):
    # Composed Elements are elements treated as a single element, but which are comprised of one or more element classes
    # They are defined here to reduce the possibility of circular dependency.

    _elements: Dict[str, Element]

    def __init__(self, window: TkWindow, name: str) -> None:
        super().__init__(window, name)
