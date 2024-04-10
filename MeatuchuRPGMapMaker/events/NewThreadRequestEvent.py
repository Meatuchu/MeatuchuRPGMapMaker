### UPDATE EVENTS ###


from typing import Callable

from .UpdateEvent import UpdateEvent


class NewThreadRequestEvent(UpdateEvent):
    # Fire this event to request a new thread from the ThreadManager
    def __init__(
        self,
        thread_name: str,
        thread_target: Callable[..., None],
        owner_id: str,
    ) -> None:
        self.thread_name = thread_name
        self.thread_target = thread_target
        self.owner_id = owner_id
        super().__init__()
