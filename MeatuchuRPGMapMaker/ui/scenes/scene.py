from tkinter import Tk as TkWindow
from typing import Callable, Dict, List, Optional, Type

from MeatuchuRPGMapMaker.events import InputSnapshotEvent
from MeatuchuRPGMapMaker.keybinds.common.close_window import CloseWindowKB
from MeatuchuRPGMapMaker.keybinds.Keybind import Keybind

from ...events.Event import Event
from ...exceptions import DuplicateSceneElementError
from ..elements.primitive_elements.base_element import Element


class Scene:
    # Scenes are descriptors of UI states - An example of a scene may be the "Export" scene, which will
    # describe the UI when exporting a Map to an image and JSON file to be loaded into foundry.

    # Attributes
    _window: TkWindow
    _elements: Dict[str, Element]
    _fire_event: Callable[[Event], None]
    _subscription_ids: List[str]
    _subscribe_to_event: Optional[Callable[[Type[Event], Callable[..., None]], str]]
    _unsubscribe_from_event: Optional[Callable[[str], None]]
    _keybinds: List[Keybind]
    name: str

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[[Event], None],
        subscribe_to_event: Optional[Callable[[Type[Event], Callable[..., None]], str]] = None,
        unsubscribe_from_event: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.name = self.__class__.__name__
        self._window = window
        self._elements = {}
        self._fire_event = fire_event
        self._subscribe_to_event = subscribe_to_event
        self._unsubscribe_from_event = unsubscribe_from_event
        self._subscription_ids = []
        self._keybinds = []

        self._add_keybind(CloseWindowKB(self._fire_event))
        self._subscribe(InputSnapshotEvent, self._input_snapshot_event_handler)

    def _add_keybind(self, kb: Keybind) -> None:
        self._keybinds.append(kb)

    def _input_snapshot_event_handler(self, event: InputSnapshotEvent) -> None:
        for kb in self._keybinds:
            kb.check(event.snapshot)

    def _subscribe(self, event_type: Type[Event], handler: Callable[..., None]) -> None:
        if self._subscribe_to_event:
            self._subscription_ids.append(self._subscribe_to_event(event_type, handler))

    def _unsubscribe(self, sid: str) -> None:
        if self._unsubscribe_from_event:
            self._unsubscribe_from_event(sid)
        self._subscription_ids.remove(sid)

    def place_element(self, e: Element) -> None:
        if self._elements.get(e.name):
            raise DuplicateSceneElementError(e.name, self.__class__.__name__)
        self._elements[e.name] = e

    def place_elements(self, es: List[Element]) -> None:
        for e in es:
            self.place_element(e)

    def unload(self) -> None:
        self._keybinds = []
        for e in self._elements.values():
            e.destroy()
        self._elements = {}
        while self._subscription_ids:
            self._unsubscribe(self._subscription_ids[0])

    def frame_update(self) -> None:
        for e in self._elements.values():
            e.frame_update()

    def tick_update(self) -> None:
        for e in self._elements.values():
            e.tick_update()
