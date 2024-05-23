from tkinter import Tk as TkWindow
from typing import Callable, Literal

from MeatuchuRPGMapMaker.events import Event

from ....exceptions import ElementCreatedWithoutWindowError, ElementNotNamedError

ElementPlacingMode = Literal["relative", "absolute"]


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
    visible = False
    x: int
    y: int
    x_offset: int
    y_offset: int
    destroyed: bool = False

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        name: str,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
    ) -> None:
        if not name:
            raise (ElementNotNamedError(self.__class__.__name__))
        if not window:
            raise (ElementCreatedWithoutWindowError(self.__class__.__name__))
        self.window = window
        self.name = name
        self._fire_event = fire_event
        self.placing_mode = placing_mode

        if place_on_creation:
            self.place()

    def handle_window_resize(self, new_width: int, new_height: int) -> None:
        if self.destroyed:
            return

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
