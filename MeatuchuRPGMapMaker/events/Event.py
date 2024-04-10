from datetime import datetime


class Event:
    # Base Event Class
    # Subscribers to this class are invoked for all events
    def __init__(self) -> None:
        self.created_at = datetime.now().timestamp()
