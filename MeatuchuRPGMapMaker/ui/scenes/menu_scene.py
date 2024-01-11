from tkinter import Tk as TkWindow
from .scene import Scene
from ..elements.primitive_elements import Button, FloatingText
from ..styles import TextStyles


class MenuScene(Scene):
    # Main menu scene :)
    def __init__(self, window: TkWindow) -> None:
        super().__init__(window)

        self.place_elements(
            [
                FloatingText(window, "mainmenu_label", "Meatuchu's RPG Map Maker", style=TextStyles.H1),
                Button(
                    window,
                    "startgamebutton",
                    "Test Button Please Ignore",
                    x=200,
                    y=200,
                    press_handler=lambda: print("pressed"),
                ),
            ]
        )
