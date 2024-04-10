from tkinter import Tk as TkWindow
from typing import Callable

from ...events.Event import Event
from ..elements.composed_elements.main_menu.options import MainMenuOptions
from ..elements.primitive_elements import FloatingText
from ..styles import TextStyles
from .scene import Scene


class MenuScene(Scene):
    # Main menu scene :)

    def __init__(self, window: TkWindow, queue_event: Callable[[Event], None]) -> None:
        super().__init__(window, queue_event)

        self.place_elements(
            [
                FloatingText(window, "title", "RPG Map Maker", style=TextStyles.H1),
                FloatingText(window, "subtitle", "  Created by Meatuchu", style=TextStyles.H3, y=65),
                MainMenuOptions(window, y=100, x=50),
            ]
        )
