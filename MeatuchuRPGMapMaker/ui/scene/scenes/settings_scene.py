from tkinter import Tk as TkWindow
from typing import Callable, Type

from MeatuchuRPGMapMaker.events import Event, LogEvent, SceneChangeRequestEvent

from ...elements.composed_elements import TabbedFrame
from ...elements.primitive_elements import Button, FloatingText
from ..scene import Scene


class SettingsScene(Scene):
    # Scene describes the UI when editing settings
    def __init__(
        self,
        window: TkWindow,
        window_name: str,
        fire_event: Callable[[Event], None],
        subscribe_to_event: Callable[[Type[Event], Callable[..., None]], str] | None = None,
        unsubscribe_from_event: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(window, window_name, fire_event, subscribe_to_event, unsubscribe_from_event)

        self._frames = TabbedFrame(
            window,
            "SettingsSceneTabbedFrame",
            fire_event,
            sizing_mode="relative",
            placing_mode="absolute",
            height=100,
            width=100,
            x=15,
            width_offset=-30,
            height_offset=-35,
        )
        self._frames.add_tab("General", "general_tab")
        self._frames.add_tab("Video", "video_tab")
        self._frames.add_element_to_tab(
            "general_tab",
            FloatingText(
                window,
                fire_event,
                "general_tab_text",
                "General Settings",
                placing_mode="absolute",
                place_on_creation=False,
            ),
            frame_posx=10,
            frame_posy=10,
        )
        self._frames.add_element_to_tab(
            "video_tab",
            FloatingText(
                window,
                fire_event,
                "video_tab_text",
                "Video Settings",
                placing_mode="absolute",
                place_on_creation=False,
            ),
            frame_posx=10,
            frame_posy=10,
        )

        self.place_elements(
            [
                self._frames,
                MainMenuButton(window, fire_event),
            ]
        )


class MainMenuButton(Button):
    def __init__(self, window: TkWindow, fire_event: Callable[[Event], None]) -> None:
        def press_handler() -> None:
            fire_event(LogEvent("DEBUG", "Main menu button pressed", "SettingsScene_MainMenuButton"))
            fire_event(SceneChangeRequestEvent("MenuScene"))

        super().__init__(
            window,
            fire_event,
            "mainmenubutton",
            "Return to Main Menu From Settings",
            x=100,
            y=100,
            x_offset=-266,
            y_offset=-32,
            height=30,
            width=250,
            press_handler=press_handler,
            placing_mode="relative",
            place_on_creation=True,
        )
