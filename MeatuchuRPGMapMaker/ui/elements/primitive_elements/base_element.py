from tkinter import Tk as TkWindow
from typing import Any, Callable, Literal

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.exceptions import (
    ElementCreatedWithoutWindowError,
    ElementNotNamedError,
)

ElementPlacingMode = Literal["relative", "absolute"]
ElementSizingMode = Literal["relative", "absolute"]


class Element:
    # Base class for primitive elements in the UI
    # Primitive elements are the basic building blocks of the user interface,
    # such as buttons, labels, and input fields.
    # They provide common functionality and can be customized for specific needs.
    # This class defines the common attributes and methods that all primitive elements should have.
    # Subclasses can inherit from this class and override or add additional functionality as needed.

    name: str
    _fire_event: Callable[[Event], None]
    placing_mode: ElementPlacingMode
    sizing_mode: ElementSizingMode
    visible = False
    x: int
    y: int
    x_offset: int
    y_offset: int
    height: int
    width: int
    height_offset: int = 0
    width_offset: int = 0
    destroyed: bool = False

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event | dict[str, Any]], None],
        name: str,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
        sizing_mode: ElementSizingMode = "absolute",
    ) -> None:
        if not name:
            raise (ElementNotNamedError(self.__class__.__name__))
        if not window:
            raise (ElementCreatedWithoutWindowError(self.__class__.__name__))
        self.window = window
        self.name = name
        self._fire_event = fire_event
        self.placing_mode = placing_mode
        self.sizing_mode = sizing_mode
        if place_on_creation:
            self.place()

    def handle_window_resize(self) -> None:
        if self.visible:
            self.place()

    def get_adjusted_wh(self) -> tuple[int, int]:
        if self.destroyed:
            return 0, 0
        if self.sizing_mode == "absolute":
            return self.width, self.height
        elif self.sizing_mode == "relative":
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            adjusted_width = int(round((self.width * window_width) / 100)) + self.width_offset
            adjusted_height = int(round((self.height * window_height) / 100)) + self.height_offset
            return adjusted_width, adjusted_height
        return 0, 0

    def place(self) -> None:
        if self.destroyed:
            return
        self.visible = True

    def hide(self) -> None:
        if self.destroyed:
            return
        self.visible = False

    def move_to(self, x: int, y: int, x_offset: int = 0, y_offset: int = 0) -> None:
        """Move the element to the specified position"""
        if self.destroyed:
            return
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        if self.visible:
            self.place()

    def destroy(self) -> None:
        self.visible = False
        self.destroyed = True

    def frame_update(self) -> None:
        """Called every frame"""
        if self.destroyed:
            return
        pass

    def tick_update(self) -> None:
        """Called every tick"""
        if self.destroyed:
            return
        pass
