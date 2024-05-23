from tkinter import Frame as TkFrame
from tkinter import Tk as TkWindow
from typing import Callable

from .base_element import Element, ElementPlacingMode


class Frame(Element):
    _label: str
    x: int
    y: int
    width: int
    height: int
    _tkframe: TkFrame

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[..., None],
        name: str,
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        background: str = "#D9D9D9",
        width: int = 300,
        height: int = 50,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self._tkframe = TkFrame(
            master=window,
            borderwidth=2,
            relief="raised",
            background=background,
        )
        super().__init__(window, fire_event, name, place_on_creation=place_on_creation, placing_mode=placing_mode)

    def place(self) -> None:
        self._tkframe.place(x=self.x, y=self.y, width=self.width, height=self.height)
        if self.placing_mode == "absolute":
            self._tkframe.place(
                x=self.x + self.x_offset,
                y=self.y + self.y_offset,
                width=self.width,
                height=self.height,
            )
        elif self.placing_mode == "relative":
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            position_x = (self.x * self.window.winfo_width() / 100) + self.x_offset
            position_y = (self.y * self.window.winfo_height() / 100) + self.y_offset
            self._tkframe.place(
                x=max(position_x, window_width, 0),
                y=max(position_y, window_height, 0),
                width=self.width,
                height=self.height,
            )

    def destroy(self) -> None:
        self._tkframe.destroy()
        return super().destroy()

    def hide(self) -> None:
        self._tkframe.place_forget()
