from .InputEvent import InputEvent


class MouseScrollEvent(InputEvent):
    # Fired when the mousewheel is scrolled
    def __init__(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
    ) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        super().__init__()
