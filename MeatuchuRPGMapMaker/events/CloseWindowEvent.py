from typing import Optional

from .UpdateEvent import UpdateEvent


class CloseWindowEvent(UpdateEvent):
    # Fired when a window is closed
    def __init__(self, window_name: Optional[str] = None) -> None:
        self.window_name = window_name
        super().__init__()
