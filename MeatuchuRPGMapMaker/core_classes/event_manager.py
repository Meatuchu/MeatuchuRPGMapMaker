from typing import Dict, List, Callable, Literal, Type
import sys

from . import FeatureManager
from .events import Event, InputEvent, RenderEvent, UpdateEvent, AppShutDownEvent


class EventManager(FeatureManager):
    _subscriptions: Dict[str, List[Callable[..., None]]]
    _input_event_queue: List[InputEvent]
    _update_event_queue: List[UpdateEvent]
    _render_event_queue: List[RenderEvent]
    _misc_event_queue: List[Event]

    def __init__(
        self,
    ) -> None:
        self._event_defs = {}
        self._subscriptions = {}
        self._misc_event_queue = []
        self._input_event_queue = []
        self._update_event_queue = []
        self._render_event_queue = []
        super().__init__()

    def register_subscription(self, event_class: Type[Event], function: Callable[..., None]) -> None:
        target = event_class.name
        self._subscriptions[target] = self._subscriptions.get(target, list())
        self._subscriptions[target].append(function)

    def queue_event(self, event: Event) -> None:
        self.log("DEBUG", f"Adding event {event.name} to event queue")
        if isinstance(event, InputEvent):
            self._input_event_queue.append(event)
        elif isinstance(event, UpdateEvent):
            self._update_event_queue.append(event)
        elif isinstance(event, RenderEvent):
            self._render_event_queue.append(event)
        else:
            self._misc_event_queue.append(event)

    def process_next_event(self, event_type: Literal["input", "update", "render", None]) -> None:
        if event_type is "input":
            q = self._input_event_queue
        elif event_type is "update":
            q = self._update_event_queue
        elif event_type is "render":
            q = self._render_event_queue
        else:
            q = self._misc_event_queue

        event = q.pop(0)
        subscribers = self._subscriptions.get(event.name, []) + self._subscriptions.get(Event.name, [])

        if subscribers:
            self.log(
                "INFO",
                f"Begin processing event {event.name} ({len(subscribers)} subscribers)",
            )

        for subscriber in subscribers:
            subscriber(event)

        if event.name == AppShutDownEvent.name:
            sys.exit()

    def input_step(self, frame_number: int) -> None:
        if not self._input_event_queue:
            return
        self.log("DEBUG", "processing all input events...")
        while self._input_event_queue:
            self.process_next_event("input")
        return super().input_step(frame_number)

    def update_step(self, frame_number: int) -> None:
        if not self._update_event_queue and not self._misc_event_queue:
            return
        self.log("DEBUG", "processing all update events...")
        while self._update_event_queue:
            self.process_next_event("update")
        self.log("DEBUG", "processing all misc events...")
        while self._misc_event_queue:
            self.process_next_event(None)
        return super().update_step(frame_number)

    def render_step(self, frame_number: int) -> None:
        if not self._render_event_queue:
            return
        self.log("DEBUG", "processing all render events...")
        while self._render_event_queue:
            self.process_next_event("render")
        return super().render_step(frame_number)
