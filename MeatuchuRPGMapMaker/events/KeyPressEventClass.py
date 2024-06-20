from .InputEventClass import InputEvent


class KeyPressEvent(InputEvent):
    # Fired when any key is pressed
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__()
