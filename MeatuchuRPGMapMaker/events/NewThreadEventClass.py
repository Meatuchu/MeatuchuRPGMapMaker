from .UpdateEventClass import UpdateEvent


class NewThreadEvent(UpdateEvent):
    # Fired when a thread is created
    def __init__(
        self,
        thread_name: str,
    ) -> None:
        self.thread_name = thread_name
        super().__init__()
