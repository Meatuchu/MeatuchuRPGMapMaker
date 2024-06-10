class InputSnapshot:
    keys: dict[str, int]
    mouse_buttons: dict[str, dict[str, tuple[int, int] | int]]
    mouse_position: tuple[int, int]

    def __init__(
        self,
        keys: dict[str, int],
        mouse_buttons: dict[str, dict[str, tuple[int, int] | int]],
        mouse_position: tuple[int, int],
    ) -> None:
        self.keys = keys
        self.mouse_buttons = mouse_buttons
        self.mouse_position = mouse_position
