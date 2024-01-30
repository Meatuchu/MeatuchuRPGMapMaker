from tkinter import Tk as TkWindow
from .scene import Scene
from ..elements.primitive_elements import FloatingText
from ..elements.composed_elements.main_menu.options import MainMenuOptions
from ..styles import TextStyles


class MenuScene(Scene):
    # Main menu scene :)

    def __init__(self, window: TkWindow) -> None:
        super().__init__(window)

        self.place_elements(
            [
                FloatingText(window, "title", "RPG Map Maker", style=TextStyles.H1),
                FloatingText(window, "subtitle", "  Created by Meatuchu", style=TextStyles.H3, y=65),
                MainMenuOptions(window, y=100, x=50),
            ]
        )
