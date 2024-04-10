from tkinter import Tk as TkWindow
from typing import Callable, Dict, List

from ...events.Event import Event
from ...exceptions import DuplicateSceneElementError
from ..elements.primitive_elements.base_element import Element


class Scene:
    # Scenes are descriptors of UI states - An example of a scene may be the "Export" scene, which will
    # describe the UI when exporting a Map to an image and JSON file to be loaded into foundry.

    # Attributes
    _window: TkWindow
    _elements: Dict[str, Element]
    _queue_event: Callable[[Event], None]
    name: str

    def __init__(self, window: TkWindow, queue_event: Callable[[Event], None]) -> None:
        self.name = self.__class__.__name__
        self._window = window
        self._elements = {}
        self._queue_event = queue_event

    def place_element(self, e: Element) -> None:
        if self._elements.get(e.name):
            raise DuplicateSceneElementError(e.name, self.__class__.__name__)
        self._elements[e.name] = e

    def place_elements(self, es: List[Element]) -> None:
        for e in es:
            self.place_element(e)

    def unload(self) -> None:
        for e in self._elements.values():
            e.destroy()
        self._elements = {}

    def frame_update(self) -> None:
        for e in self._elements.values():
            e.frame_update()

    def tick_update(self) -> None:
        for e in self._elements.values():
            e.tick_update()
