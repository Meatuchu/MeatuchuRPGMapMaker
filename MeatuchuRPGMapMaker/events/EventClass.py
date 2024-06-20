from datetime import datetime
from typing import Any, Self


class Event:
    # Base Event Class
    # Subscribers to this class are invoked for all events
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        data.pop("name", None)
        return cls(**data)

    def __init__(self) -> None:
        self.created_at = datetime.now().timestamp()
