from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events.EventClass import EventQueueItemType
from MeatuchuRPGMapMaker.ui.elements.composed_elements.composed_element import (
    ComposedElement,
)


class MapCanvas(ComposedElement):
    def __init__(self, window: TkWindow, fire_event: Callable[[EventQueueItemType], None]) -> None:
        super().__init__(
            window,
            "mapcanvas",
            fire_event,
        )
