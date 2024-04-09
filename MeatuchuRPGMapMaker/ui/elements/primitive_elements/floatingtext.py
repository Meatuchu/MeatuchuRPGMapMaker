from tkinter import Label as TkLabel
from tkinter import Tk as TkWindow
from typing import Type

from ...styles import TextStyles
from .base_element import Element


class FloatingText(Element):
    _text: str
    _tktext: TkLabel

    def __init__(
        self,
        window: TkWindow,
        name: str,
        text: str,
        x: int = 0,
        y: int = 0,
        style: Type[TextStyles.TextStyle] = TextStyles.Normal,
    ) -> None:
        self._text = text
        self.x = x
        self.y = y
        self._tktext = TkLabel(window, text=text)
        self._tktext.config(font=(style.FONT, style.SIZE))
        self._tktext.place(x=x, y=y)
        super().__init__(window, name)

    def destroy(self) -> None:
        self._tktext.destroy()
        return super().destroy()
