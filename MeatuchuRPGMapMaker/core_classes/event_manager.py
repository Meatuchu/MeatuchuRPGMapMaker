import sys
import time
from typing import Callable, Dict, List, Literal, Tuple, Type, cast
from uuid import uuid4

from sortedcontainers import SortedDict  # pyright: ignore[reportMissingTypeStubs]

from MeatuchuRPGMapMaker.constants import NS_PER_S
from MeatuchuRPGMapMaker.events import (
    AppShutDownEvent,
    Event,
    InputEvent,
    InputSnapshotEvent,
    KeyPressEvent,
    LogEvent,
    MouseMoveEvent,
    RenderEvent,
    ThreadErrorEvent,
    UpdateEvent,
)

from . import FeatureManager

# Processing of Events in this list will not be logged
HIDDEN_EVENTS = [InputSnapshotEvent, MouseMoveEvent, LogEvent]

# Events in this list will be processed immediately upon being queued
IMMEDIATE_EVENTS = [
    AppShutDownEvent,
    ThreadErrorEvent,
    LogEvent,
]


class EventSubcriber:
    id: str
    fn: Callable[..., None]

    def __init__(self, fn: Callable[..., None]) -> None:
        self.id = str(uuid4())
        self.fn = fn


class EventManager(FeatureManager):
    _subscriptions: Dict[str, List[EventSubcriber]]
    _input_event_queue: List[InputEvent]
    _update_event_queue: List[UpdateEvent]
    _render_event_queue: List[RenderEvent]
    _misc_event_queue: List[Event]
    _scheduled_events: SortedDict
    __app_shutdown_fired: bool = False
    __app_shutdown_time: float = 0

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._event_defs = {}
        self._subscriptions = {}
        self._misc_event_queue = []
        self._input_event_queue = []
        self._update_event_queue = []
        self._render_event_queue = []
        self._scheduled_events = SortedDict()
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        def handle_log_event(event: LogEvent) -> None:
            self._logger.log(event.msg_level, event.msg, event.src)

        self.register_subscription(LogEvent, handle_log_event)

    def register_subscription(self, event_class: Type[Event], function: Callable[..., None]) -> str:
        subscriber = EventSubcriber(function)
        target = event_class.__name__
        self.log("INFO", f"registering subscriber to {target}")
        self._subscriptions[target] = self._subscriptions.get(target, list())
        self._subscriptions[target].append(subscriber)
        return subscriber.id

    def unregister_subscription(self, subscriber_id: str) -> None:
        for subscribers in self._subscriptions.values():
            for subscriber in subscribers:
                if subscriber.id == subscriber_id:
                    subscribers.remove(subscriber)
                    return

    def schedule_event(self, event: Event, delay_sec: float) -> None:
        self.log("DEBUG", f"Scheduling event {event.__class__.__name__} to run in {delay_sec} seconds")

        timestamp = time.time() + delay_sec
        events_at_time: List[Event] = cast(
            List[Event],
            self._scheduled_events.get(timestamp, []),  # pyright: ignore[reportUnknownMemberType]
        )
        events_at_time.append(event)
        self._scheduled_events[timestamp] = events_at_time

    def queue_scheduled_events(self) -> None:
        # makes pylance happy
        peekitem = cast(Callable[[int], Tuple[float, List[Event]]], self._scheduled_events.peekitem)
        popitem = cast(Callable[[int], Tuple[float, List[Event]]], self._scheduled_events.popitem)

        current_time = time.time()
        while self._scheduled_events and peekitem(0)[0] < current_time:
            _, events = popitem(0)
            for event in events:
                self.log(
                    "DEBUG", f"Adding event {event.__class__.__name__} to event queue to be processed at next tick"
                )
                self.queue_event(event)

    def queue_event(self, event: Event) -> None:
        if self.__app_shutdown_fired:
            if isinstance(event, AppShutDownEvent):
                return
            self.log("ERROR", f"App is shutting down, unable to handle queued event {event.__class__.__name__}")
            return

        self._log_event_handle_info(event, "DEBUG", f"Adding event {event.__class__.__name__} to event queue")

        if isinstance(event, AppShutDownEvent):
            self.__app_shutdown_fired = True
            self.__app_shutdown_time = time.time_ns()
            discarding_events = (
                self._input_event_queue
                + self._update_event_queue
                + self._render_event_queue
                + self._misc_event_queue
                + list(self._scheduled_events.values())
            )
            if discarding_events:
                c = len(discarding_events)
                self.log(
                    "ERROR",
                    f"App is shutting down, {len(discarding_events)} event{'s' if c > 1 else ''} will not be processed",
                )
                [self.log("WARNING", f"Discarding event {e.__class__.__name__}") for e in discarding_events]

        for t in IMMEDIATE_EVENTS:
            if isinstance(event, t):
                self._process_event(event)
                return

        if isinstance(event, InputEvent):
            self._input_event_queue.append(event)
        elif isinstance(event, UpdateEvent):
            self._update_event_queue.append(event)
        elif isinstance(event, RenderEvent):
            self._render_event_queue.append(event)
        else:
            self._misc_event_queue.append(event)

    def _process_event(self, event: Event) -> None:
        subscribers = self._subscriptions.get(event.__class__.__name__, [])
        if event.__class__.__name__ is not Event.__name__:
            subscribers += self._subscriptions.get(Event.__name__, [])

        if subscribers:
            self._log_event_handle_info(
                event,
                "INFO",
                f"Begin processing event {event.__class__.__name__} ({len(subscribers)} subscribers)",
            )
        else:
            self._log_event_handle_info(
                event, "VERBOSE", f"Begin processing event {event.__class__.__name__} (no subscribers)"
            )

        if isinstance(event, KeyPressEvent):
            self.log("VERBOSE", f"Key Press Event: {event.key}")

        for subscriber in subscribers:
            subscriber.fn(event)

        if isinstance(event, AppShutDownEvent):
            self.log(
                "INFO",
                "App is shutting down - Took "
                + str((time.time_ns() - self.__app_shutdown_time) / NS_PER_S)
                + " seconds from AppShutDownEvent to shutdown",
            )
            sys.exit()

    def _process_next_event(self, event_type: Literal["input", "update", "render", None]) -> None:
        if event_type == "input":
            q = self._input_event_queue
        elif event_type == "update":
            q = self._update_event_queue
        elif event_type == "render":
            q = self._render_event_queue
        else:
            q = self._misc_event_queue

        self._process_event(q.pop(0))

    def input_step(self, frame_number: int) -> None:
        while self._input_event_queue:
            self._process_next_event("input")
        while self._misc_event_queue:
            self._process_next_event(None)
        return super().input_step(frame_number)

    def update_step(self, frame_number: int) -> None:
        while self._update_event_queue:
            self._process_next_event("update")
        while self._misc_event_queue:
            self._process_next_event(None)
        return super().update_step(frame_number)

    def render_step(self, frame_number: int) -> None:
        while self._render_event_queue:
            self._process_next_event("render")
        while self._misc_event_queue:
            self._process_next_event(None)
        return super().render_step(frame_number)

    def _log_event_handle_info(
        self, event: Event, level: Literal["ERROR", "WARNING", "DEBUG", "INFO", "VERBOSE"], msg: str
    ) -> None:
        if event.__class__ in [InputEvent, RenderEvent, UpdateEvent]:
            return
        for t in HIDDEN_EVENTS:
            if isinstance(event, t):
                return
        self.log(level, msg)
