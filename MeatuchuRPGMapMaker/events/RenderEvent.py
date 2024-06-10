from .Event import Event


class RenderEvent(Event):
    # Used only for events relating to rendering and windows
    window_name: str | None
