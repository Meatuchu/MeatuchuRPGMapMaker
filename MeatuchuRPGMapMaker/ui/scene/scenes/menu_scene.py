from tkinter import Tk as TkWindow

from ...elements.prefabs.main_menu.options_list import MainMenuOptions
from ...elements.primitive_elements import FloatingText
from ...styles import TextStyles
from ..scene import Scene


class MenuScene(Scene):
    # Main menu scene :)

    def __init__(
        self,
        window: TkWindow,
        window_name: str,
    ) -> None:
        super().__init__(window, window_name)

        self.place_elements(
            [
                FloatingText(window, self.fire_event, "title", "RPG Map Maker", style=TextStyles.H1),
                FloatingText(window, self.fire_event, "subtitle", "  Created by Meatuchu", style=TextStyles.H3, y=65),
                MainMenuOptions(window, self.fire_event, y=100, x=50),
            ]
        )
