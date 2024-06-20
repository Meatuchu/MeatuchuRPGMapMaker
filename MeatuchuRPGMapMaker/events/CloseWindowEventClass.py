from .UpdateEventClass import UpdateEvent


class CloseWindowEvent(UpdateEvent):
    # Fired when a window is closed
    def __init__(self, window_name: str | None = None) -> None:
        self.window_name = window_name
        super().__init__()
