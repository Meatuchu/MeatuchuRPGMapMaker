from .InputEventClass import InputEvent


class MouseClickReleaseEvent(InputEvent):
    # Fired when a mouse button is released
    def __init__(self, button: str, position: tuple[int, int], hold_time: float) -> None:
        self.button = button
        self.position = position
        self.hold_time = hold_time
        super().__init__()
