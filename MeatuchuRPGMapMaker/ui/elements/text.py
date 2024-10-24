from tkinter import Label
from tkinter import Tk as TkWindow

from .element import Element


class Text(Element):
    ALLOW_CHILDREN: bool = False
    text: str

    def __init__(self, window: TkWindow, parent: Element, text: str = "", id: str = "") -> None:
        super().__init__(window=window, parent=parent, id=id)
        self.text = text
        self.label = Label(window, text=self.text)

    def render(self) -> None:
        self.label.pack()
        pass
