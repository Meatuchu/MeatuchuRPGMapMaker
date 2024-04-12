from typing import Optional

from .RenderEvent import RenderEvent


class WindowToggleFullscreenModeRequestEvent(RenderEvent):
    # Fire this event to request a window's fullscreen mode be updated
    def __init__(self, window_name: Optional[str] = None) -> None:
        self.window_name = window_name
        super().__init__()
