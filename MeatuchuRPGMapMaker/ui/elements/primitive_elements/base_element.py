from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import Event

from ....exceptions import ElementCreatedWithoutWindowError, ElementNotNamedError


class Element:
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

    def destroy(self) -> None:
        pass

    def frame_update(self) -> None:
        """Called every frame"""
        pass

    def tick_update(self) -> None:
        """Called every tick"""
        pass
