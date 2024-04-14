from tkinter import Tk as TkWindow
from typing import Callable, Optional, Type

from ...events.Event import Event
from ..elements.composed_elements.main_menu.options_list import MainMenuOptions
from ..elements.primitive_elements import FloatingText
from ..styles import TextStyles
from .scene import Scene


class MenuScene(Scene):
    # Main menu scene :)

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        subscribe_to_event: Optional[Callable[[Type[Event], Callable[..., None]], str]] = None,
        unsubscribe_from_event: Optional[Callable[[str], None]] = None,
    ) -> None:
        super().__init__(window, fire_event, subscribe_to_event, unsubscribe_from_event)

        self.place_elements(
            [
                FloatingText(window, fire_event, "title", "RPG Map Maker", style=TextStyles.H1),
                FloatingText(window, fire_event, "subtitle", "  Created by Meatuchu", style=TextStyles.H3, y=65),
                MainMenuOptions(window, fire_event, y=100, x=50),
            ]
        )
