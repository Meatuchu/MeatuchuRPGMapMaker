from tkinter import Label as TkLabel
from tkinter import Tk as TkWindow
from typing import Callable, Type

from MeatuchuRPGMapMaker.events import Event

from ...styles import TextStyles
from .base_element import Element, ElementPlacingMode


class FloatingText(Element):
    _text: str
    _tktext: TkLabel

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        name: str,
        text: str,
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        style: Type[TextStyles.TextStyle] = TextStyles.Normal,
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        self._text = text
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self._tktext = TkLabel(window, text=text)
        self._tktext.config(font=(style.FONT, style.SIZE))
        super().__init__(window, fire_event, name, placing_mode=placing_mode)

    def place(self) -> None:
        if self.placing_mode == "absolute":
            self._tktext.place(
                x=self.x + self.x_offset,
                y=self.y + self.y_offset,
            )
        elif self.placing_mode == "relative":
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            position_x = (self.x * window_width / 100) + self.x_offset
            position_y = (self.y * window_height / 100) + self.y_offset
            self._tktext.place(
                x=max(position_x, window_width, 0),
                y=max(position_y, window_height, 0),
            )

    def destroy(self) -> None:
        self._tktext.destroy()
        return super().destroy()
