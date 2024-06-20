from .UpdateEventClass import UpdateEvent


class DestroyThreadEvent(UpdateEvent):
    # Fired when a thread is destroyed
    def __init__(self, thread_name: str) -> None:
        self.thread_name = thread_name
        super().__init__()
