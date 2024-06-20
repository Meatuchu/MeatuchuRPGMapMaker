### RENDER EVENTS ###

from .RenderEventClass import RenderEvent


class WindowResizedEvent(RenderEvent):
    # Fired when a window has been resized
    def __init__(self, width: int, height: int, window_name: str | None = None) -> None:
        self.width = width
        self.height = height
        self.window_name = window_name
        super().__init__()
