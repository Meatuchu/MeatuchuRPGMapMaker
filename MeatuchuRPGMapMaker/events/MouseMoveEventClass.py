from .InputEventClass import InputEvent


class MouseMoveEvent(InputEvent):
    # Fired when the mouse is moved
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__()
