from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import AppShutDownEvent, EventQueueItemType
from MeatuchuRPGMapMaker.events.LogEventClass import LogEvent
from MeatuchuRPGMapMaker.events.SceneChangeRequestEventClass import (
    SceneChangeRequestEvent,
)

from ...composed_elements import ComposedElement
from ...primitive_elements import Button
from ...primitive_elements.base_element import ElementPlacingMode


class MainMenuOptions(ComposedElement):
    option_btns_count: int = 0
    x: int
    y: int
    widget_width: int = 100
    padding_size: int = 5
    button_space: int = 1
    button_width: int = 100
    button_height: int = 30
    _fire_event: Callable[[EventQueueItemType], None]

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[EventQueueItemType], None],
        x: int = 0,
        y: int = 0,
        name: str = "mainmenuoptions",
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        super().__init__(window, name, fire_event, placing_mode=placing_mode)
        self.x = x
        self.y = y

        self.add_option_item(StartButton(window, fire_event))
        self.add_option_item(SettingsButton(window, fire_event))
        self.add_option_item(
            Button(
                window,
                fire_event,
                "exitbutton",
                "Exit",
                press_handler=lambda: fire_event(AppShutDownEvent()),
                place_on_creation=False,
            )
        )

    def add_option_item(self, element: Button) -> None:
        try:
            self.add_element(element)
            element.height = self.button_height
            element.width = self.button_width
            element.x = self.x + self.padding_size
            element.y = self.y + self.padding_size + (self.option_btns_count * (element.height + self.button_space))
            element.place()
            self.option_btns_count += 1
        except ValueError as e:
            self._fire_event(LogEvent("ERROR", str(e), "MainMenuOptions_add_option_item"))

    def tick_update(self) -> None:
        super().tick_update()


class StartButton(Button):
    def __init__(
        self, window: TkWindow, fire_event: Callable[[EventQueueItemType], None], x: int = 0, y: int = 0
    ) -> None:
        def press_handler() -> None:
            fire_event(SceneChangeRequestEvent("MapEditScene"))

        super().__init__(
            window,
            fire_event,
            "startbutton",
            "Start",
            x=x + 5,
            y=y + 5,
            height=30,
            width=100,
            press_handler=press_handler,
            place_on_creation=False,
        )


class SettingsButton(Button):
    def __init__(
        self, window: TkWindow, fire_event: Callable[[EventQueueItemType], None], x: int = 0, y: int = 0
    ) -> None:
        def press_handler() -> None:
            fire_event(SceneChangeRequestEvent("SettingsScene"))

        super().__init__(
            window,
            fire_event,
            "settingsbutton",
            "Settings",
            x=x,
            y=y,
            height=30,
            width=100,
            press_handler=press_handler,
            place_on_creation=False,
        )
