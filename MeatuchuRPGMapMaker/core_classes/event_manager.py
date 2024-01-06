from typing import Dict, List, Callable, Literal, Type
import sys

from . import FeatureManager
from . import events as Events
from .events import Event, InputEvent, UpdateEvent, RenderEvent

# Events in this list will not be logged
HIDDEN_EVENTS = [Events.InputSnapshotEvent, Events.MouseMoveEvent]


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
        target = event_class.__name__
        self.log("WARNING", f"registering subscriber to {target}")
        self._subscriptions[target] = self._subscriptions.get(target, list())
        self._subscriptions[target].append(function)

    def queue_event(self, event: Event) -> None:
        self.log_event(event, "DEBUG", f"Adding event {event.__class__.__name__} to event queue")
        if isinstance(event, Events.ThreadErrorEvent):
            self.process_event(event)
            return

        if isinstance(event, InputEvent):
            self._input_event_queue.append(event)
        elif isinstance(event, UpdateEvent):
            self._update_event_queue.append(event)
        elif isinstance(event, RenderEvent):
            self._render_event_queue.append(event)
        else:
            self._misc_event_queue.append(event)

    def process_event(self, event: Event) -> None:
        subscribers = self._subscriptions.get(event.__class__.__name__, [])
        if event.__class__.__name__ is not Event.__name__:
            subscribers += self._subscriptions.get(Event.__name__, [])

        if subscribers:
            self.log_event(
                event,
                "INFO",
                f"Begin processing event {event.__class__.__name__} ({len(subscribers)} subscribers)",
            )

        for subscriber in subscribers:
            subscriber(event)

        if isinstance(event, Events.AppShutDownEvent):
            sys.exit()

    def process_next_event(self, event_type: Literal["input", "update", "render", None]) -> None:
        if event_type is "input":
            q = self._input_event_queue
        elif event_type is "update":
            q = self._update_event_queue
        elif event_type is "render":
            q = self._render_event_queue
        else:
            q = self._misc_event_queue

        self.process_event(q.pop(0))

    def input_step(self, frame_number: int) -> None:
        while self._misc_event_queue:
            self.process_next_event(None)
        while self._input_event_queue:
            self.process_next_event("input")
        return super().input_step(frame_number)

    def update_step(self, frame_number: int) -> None:
        while self._misc_event_queue:
            self.process_next_event(None)
        while self._update_event_queue:
            self.process_next_event("update")
        return super().update_step(frame_number)

    def render_step(self, frame_number: int) -> None:
        while self._misc_event_queue:
            self.process_next_event(None)
        while self._render_event_queue:
            self.process_next_event("render")
        return super().render_step(frame_number)

    def log_event(self, event: Event, level: Literal["ERROR", "WARNING", "DEBUG", "INFO"], msg: str) -> None:
        if event.__class__ in [InputEvent, RenderEvent, UpdateEvent]:
            return
        for t in HIDDEN_EVENTS:
            if isinstance(event, t):
                return
        self.log(level, msg)
