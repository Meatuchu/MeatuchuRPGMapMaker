from tkinter import Tk as TkWindow
from typing import Callable, Type

from MeatuchuRPGMapMaker.events import EventQueueItemType, InputSnapshotEvent
from MeatuchuRPGMapMaker.keybinds.common.close_window import CloseWindowKB
from MeatuchuRPGMapMaker.keybinds.common.fullscreen import FullScreenKB
from MeatuchuRPGMapMaker.keybinds.Keybind import Keybind

from ...events.EventClass import Event
from ...exceptions import DuplicateSceneElementError
from ..elements.primitive_elements.base_element import Element


class Scene:
    # Scenes are descriptors of UI states - An example of a scene may be the "Export" scene, which will
    # describe the UI when exporting a Map to an image and JSON file to be loaded into foundry.

    # Attributes
    _window: TkWindow
    _window_name: str
    _elements: dict[str, Element]
    fire_event: Callable[[EventQueueItemType], None]
    _subscription_ids: list[str]
    _subscribe_to_event: Callable[[Type[Event], Callable[..., None]], str]
    _unsubscribe_from_event: Callable[[str], None]
    _keybinds: list[Keybind]
    name: str

    def __init__(
        self,
        window: TkWindow,
        window_name: str,
    ) -> None:
        self.name = self.__class__.__name__
        self._window = window
        self._window_name = window_name
        self._elements = {}
        self._subscription_ids = []
        self._keybinds = []
        self.fire_event = self.__class__.fire_event
        self._subscribe_to_event = self.__class__._subscribe_to_event
        self._unsubscribe_from_event = self.__class__._unsubscribe_from_event

        self.add_keybind(CloseWindowKB(self.fire_event))
        self.add_keybind(FullScreenKB(self.fire_event))
        self.subscribe(InputSnapshotEvent, self.__input_snapshot_event_handler)

    @classmethod
    def inject_queue_event(cls, fn: Callable[[EventQueueItemType], None]) -> None:
        cls.fire_event = fn

    @classmethod
    def inject_subscribe_to_event(cls, fn: Callable[[Type[Event], Callable[..., None]], str]) -> None:
        cls._subscribe_to_event = fn

    @classmethod
    def inject_unsubscribe_from_event(cls, fn: Callable[[str], None]) -> None:
        cls._unsubscribe_from_event = fn

    def add_keybind(self, kb: Keybind) -> None:
        self._keybinds.append(kb)

    def __input_snapshot_event_handler(self, event: InputSnapshotEvent) -> None:
        for kb in self._keybinds:
            kb.check(event.snapshot)

    def handle_window_resize(self) -> None:
        for e in self._elements.values():
            e.handle_window_resize()

    def subscribe(self, event_type: Type[Event], handler: Callable[..., None]) -> None:
        self._subscription_ids.append(self._subscribe_to_event(event_type, handler))

    def unsubscribe(self, subscription_id: str) -> None:
        self._unsubscribe_from_event(subscription_id)
        self._subscription_ids.remove(subscription_id)

    def place_element(self, e: Element) -> None:
        if self._elements.get(e.name):
            raise DuplicateSceneElementError(e.name, self.__class__.__name__)
        self._elements[e.name] = e

    def place_elements(self, es: list[Element]) -> None:
        for e in es:
            self.place_element(e)

    def unload(self) -> None:
        self._keybinds = []
        for e in self._elements.values():
            e.destroy()
        self._elements = {}
        while self._subscription_ids:
            self.unsubscribe(self._subscription_ids[0])

    def frame_update(self) -> None:
        for e in self._elements.values():
            e.frame_update()

    def tick_update(self) -> None:
        for e in self._elements.values():
            e.tick_update()
