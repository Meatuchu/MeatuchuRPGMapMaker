from .InputEvent import InputEvent


class KeyReleaseEvent(InputEvent):
    # Fired when any key is pressed
    def __init__(self, key: str, hold_time: float) -> None:
        self.key = key
        self.hold_time = hold_time
        super().__init__()
