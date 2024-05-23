from tkinter import Frame as TkFrame
from tkinter import Tk as TkWindow
from typing import Callable

from .base_element import Element, ElementPlacingMode, ElementSizingMode


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
        height_offset: int = 0,
        width_offset: int = 0,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
        sizing_mode: ElementSizingMode = "absolute",
    ) -> None:
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.height_offset = height_offset
        self.width_offset = width_offset
        self.frame_bordersize = 2
        self._tkframe = TkFrame(
            master=window,
            borderwidth=2,
            relief="raised",
            background=background,
        )
        super().__init__(
            window,
            fire_event,
            name,
            place_on_creation=place_on_creation,
            placing_mode=placing_mode,
            sizing_mode=sizing_mode,
        )

    def place(self) -> None:
        width, height = self.get_adjusted_wh()
        if self.placing_mode == "absolute":
            self._tkframe.place(
                x=self.x + self.x_offset,
                y=self.y + self.y_offset,
                width=width,
                height=height,
            )
        elif self.placing_mode == "relative":
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            position_x = (self.x * window_width / 100) + self.x_offset
            position_y = (self.y * window_height / 100) + self.y_offset
            self._tkframe.place(
                x=position_x,
                y=position_y,
                width=width,
                height=height,
            )
        return super().place()

    def destroy(self) -> None:
        self._tkframe.destroy()
        return super().destroy()

    def hide(self) -> None:
        self._tkframe.place_forget()
        return super().hide()
