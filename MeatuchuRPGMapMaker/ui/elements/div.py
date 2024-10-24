from tkinter import Tk as TkWindow

from .element import Element


class Div(Element):
    ALLOW_CHILDREN: bool = True

    def __init__(self, window: TkWindow, parent: Element) -> None:
        super().__init__(window=window, parent=parent)

    def render(self) -> None:
        pass
