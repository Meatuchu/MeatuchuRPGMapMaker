from typing import Dict, Tuple, Union


class InputSnapshot:
    keys: Dict[str, int]
    mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]]
    mouse_position: Tuple[int, int]

    def __init__(
        self,
        keys: Dict[str, int],
        mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]],
        mouse_position: Tuple[int, int],
    ) -> None:
        self.keys = keys
        self.mouse_buttons = mouse_buttons
        self.mouse_position = mouse_position
