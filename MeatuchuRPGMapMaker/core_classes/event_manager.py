from typing import Dict, List, Callable, Type
import sys

from . import FeatureManager
from .events import Event, AppShutDownEvent


class EventManager(FeatureManager):
    _subscriptions: Dict[str, List[Callable[..., None]]]
    _event_queue: List[Event]

    def __init__(
        self,
    ) -> None:
        self._event_defs = {}
        self._subscriptions = {}
        self._event_queue = []
        super().__init__()

    def register_subscription(self, event_class: Type[Event], function: Callable[..., None]) -> None:
        target = event_class.name
        self._subscriptions[target] = self._subscriptions.get(target, list())
        self._subscriptions[target].append(function)

    def queue_event(self, event: Event) -> None:
        self.log("DEBUG", f"Adding event {event.name} to event queue")
        self._event_queue.append(event)

    def process_next_event(self) -> None:
        event = self._event_queue.pop(0)
        subscribers = self._subscriptions.get(event.name, []) + self._subscriptions.get(Event.name, [])

        if subscribers:
            self.log(
                "INFO",
                f"Begin processing event {event.name} ({len(subscribers)} subscribers)",
            )

        for subscriber in subscribers:
            subscriber(*event.args, **event.kwargs)

        if event.name == AppShutDownEvent.name:
            sys.exit()

    def process_all_events(self) -> None:
        if not self._event_queue:
            return
        self.log("DEBUG", "processing all events...")
        while self._event_queue:
            self.process_next_event()
