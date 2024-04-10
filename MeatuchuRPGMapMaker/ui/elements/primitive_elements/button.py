from tkinter import Button as TkButton
from tkinter import Tk as TkWindow
from typing import Callable

from .base_element import Element


class Button(Element):
    _label: str
    x: int
    y: int
    width: int
    height: int
    _press_handler: Callable[..., None]
    _tkinter_button: TkButton

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[..., None],
        name: str,
        label: str = "Button",
        x: int = 0,
        y: int = 0,
        width: int = 300,
        height: int = 50,
        press_handler: Callable[..., None] = lambda: None,
    ) -> None:
        super().__init__(window, fire_event, name)
        self._label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.set_press_handler(press_handler)
        self._tkinter_button = TkButton(
            master=window,
            text=label,
            command=self.press_handler,
        )
        self._tkinter_button.place(x=x, y=y)

    def set_press_handler(self, handler: Callable[..., None]) -> None:
        self._press_handler = handler

    def press_handler(self) -> None:
        self._press_handler()

    def destroy(self) -> None:
        self._tkinter_button.destroy()
        return super().destroy()
