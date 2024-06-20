### EXCEPTION EVENTS ###
from .EventClass import Event


class ThreadErrorEvent(Event):
    # Base class for thread errors
    def __init__(self, thread_name: str, owner_id: str, exception: Exception) -> None:
        self.thread_name = thread_name
        self.owner_id = owner_id
        self.exception = exception
        super().__init__()
