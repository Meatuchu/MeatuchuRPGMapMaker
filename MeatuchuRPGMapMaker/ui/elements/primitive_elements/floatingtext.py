from tkinter import Label as TkLabel
from tkinter import Tk as TkWindow
from typing import Callable, Type

from MeatuchuRPGMapMaker.events import EventQueueItemType

from ...styles import TextStyles
from .base_element import Element, ElementPlacingMode, ElementSizingMode


class FloatingText(Element):
    _text: str
    _tktext: TkLabel

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[EventQueueItemType], None],
        name: str,
        text: str,
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        style: Type[TextStyles.TextStyle] = TextStyles.Normal,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
        sizing_mode: ElementSizingMode = "absolute",
    ) -> None:
        self._text = text
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self._tktext = TkLabel(window, text=text)
        self._tktext.config(font=(style.FONT, style.SIZE))
        super().__init__(
            window,
            fire_event,
            name,
            placing_mode=placing_mode,
            place_on_creation=place_on_creation,
            sizing_mode=sizing_mode,
        )

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
        return super().place()

    def hide(self) -> None:
        self._tktext.place_forget()
        return super().hide()

    def destroy(self) -> None:
        self._tktext.destroy()
        return super().destroy()
