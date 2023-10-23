from typing import Callable

from .base_element import Element


class Button(Element):
    label: str
    x: int
    y: int
    width: int
    height: int
    _press_handler: Callable[..., None] = lambda: None
    pressed: bool = False

    def __init__(
        self,
        label: str = "Button",
        x: int = 0,
        y: int = 0,
        width: int = 300,
        height: int = 50,
    ) -> None:
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_press_handler(self, handler: Callable[..., None]) -> None:
        self._press_handler = handler

    def press_handler(self) -> None:
        self._press_handler()
