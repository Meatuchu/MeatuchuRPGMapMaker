from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import Event

from ....exceptions import ElementCreatedWithoutWindowError, ElementNotNamedError


class Element:
    # Base class for primitive elements in the UI
    # Primitive elements are the basic building blocks of the user interface,
    # such as buttons, labels, and input fields.
    # They provide common functionality and can be customized for specific needs.
    # This class defines the common attributes and methods that all primitive elements should have.
    # Subclasses can inherit from this class and override or add additional functionality as needed.

    name: str
    _fire_event: Callable[[Event], None]

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        name: str,
    ) -> None:
        if not name:
            raise (ElementNotNamedError(self.__class__.__name__))
        if not window:
            raise (ElementCreatedWithoutWindowError(self.__class__.__name__))
        self.name = name
        self._fire_event = fire_event

    def place(self) -> None:
        pass

    def move_to(self, x: int, y: int) -> None:
        """Move the element to the specified position"""
        pass

    def destroy(self) -> None:
        pass

    def frame_update(self) -> None:
        """Called every frame"""
        pass

    def tick_update(self) -> None:
        """Called every tick"""
        pass
