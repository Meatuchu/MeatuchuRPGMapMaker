from .InputEvent import InputEvent


class MouseClickEvent(InputEvent):
    # Fired when a mouse button is pressed
    def __init__(self, button: str, position: tuple[int, int]) -> None:
        self.button = button
        self.position = position
        super().__init__()
