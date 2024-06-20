from datetime import datetime
from typing import Any, Callable, Self


class Event:
    # Base Event Class
    # Subscribers to this class are invoked for all events
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        data.pop("name", None)
        return cls(**data)

    def __init__(self) -> None:
        self.created_at = datetime.now().timestamp()


type EventQueueItemType = Event | dict[str, Any]
type EventQueueType = list[EventQueueItemType]
type AddToEventQueueFuncType = Callable[[EventQueueItemType], None]
type EventSubscriptionArgType = type[Event] | str
