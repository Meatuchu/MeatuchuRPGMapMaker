### RENDER EVENTS ###

from .RenderEvent import RenderEvent


class WindowResizeRequestEvent(RenderEvent):
    # Fired to request a window resize
    def __init__(self, width: int, height: int, window_name: str | None = None) -> None:
        self.width = width
        self.height = height
        self.window_name = window_name
        super().__init__()
