from .UpdateEventClass import UpdateEvent


class DestroyThreadRequestEvent(UpdateEvent):
    # Fire this event to request ThreadManager to destroy a thread
    def __init__(self, thread_name: str, owner_id: str) -> None:
        self.thread_name = thread_name
        self.owner_id = owner_id
        super().__init__()
