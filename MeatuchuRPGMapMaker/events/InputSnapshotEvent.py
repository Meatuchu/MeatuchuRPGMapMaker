### INPUT EVENTS ###


from typing import Dict, Tuple, Union

from .InputEvent import InputEvent


class InputSnapshotEvent(InputEvent):
    # Emitted by InputManager on every input step - subscribe to this to get a collection of the current state of input
    def __init__(
        self,
        keys: Dict[str, int],
        mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]],
        mouse_position: Tuple[int, int],
    ) -> None:
        self.keys = keys
        self.mouse_buttons = mouse_buttons
        self.mouse_postion = mouse_position
        super().__init__()
