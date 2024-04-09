from tkinter import Tk as TkWindow

from ....elements.primitive_elements import Button
from .. import ComposedElement


class MainMenuOptions(ComposedElement):
    def __init__(self, window: TkWindow, x: int = 0, y: int = 0, name: str = "mainmenuoptions") -> None:
        super().__init__(window, name=name)

        self._elements = {
            "startbutton": Button(
                window,
                "startbutton",
                "Start",
                x=x + 5,
                y=y + 5,
                press_handler=lambda: print("pressed"),
            ),
        }

    def tick_update(self) -> None:
        super().tick_update()
