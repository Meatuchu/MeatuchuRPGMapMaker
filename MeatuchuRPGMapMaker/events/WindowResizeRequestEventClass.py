### RENDER EVENTS ###

from .RenderEventClass import RenderEvent


class WindowResizeRequestEvent(RenderEvent):
    # Fired to request a window resize
    def __init__(self, width: int | None, height: int | None, window_name: str | None = None) -> None:
        self.width = width
        self.height = height
        self.window_name = window_name
        super().__init__()
