from tkinter import Frame as TkFrame
from tkinter import Tk as TkWindow
from typing import Callable

from .base_element import Element


class Frame(Element):
    _label: str
    x: int
    y: int
    width: int
    height: int
    _tkinter_frame: TkFrame

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[..., None],
        name: str,
        x: int = 0,
        y: int = 0,
        background: str = "#D9D9D9",
        width: int = 300,
        height: int = 50,
        place_on_creation: bool = True,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._tkinter_frame = TkFrame(
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
        )

    def place(self) -> None:
        self._tkinter_frame.place(x=self.x, y=self.y, width=self.width, height=self.height)

    def destroy(self) -> None:
        self._tkinter_frame.destroy()
        return super().destroy()

    def hide(self) -> None:
        print("????")
        self._tkinter_frame.pack_forget()
        self._tkinter_frame.grid_remove()
