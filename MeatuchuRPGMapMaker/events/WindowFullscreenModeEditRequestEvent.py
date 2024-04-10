from typing import Literal, Optional

from .RenderEvent import RenderEvent


class WindowFullscreenModeEditRequestEvent(RenderEvent):
    # Fire this event to request a window's fullscreen mode be updated
    def __init__(self, mode: Literal[0, 1, 2], window_name: Optional[str] = None) -> None:
        self.mode = mode
        self.window_name = window_name
        super().__init__()
