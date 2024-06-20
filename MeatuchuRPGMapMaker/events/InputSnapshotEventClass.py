from ..classes.input_snapshot import InputSnapshot
from .InputEventClass import InputEvent


class InputSnapshotEvent(InputEvent):
    # Emitted by InputManager on every input step - subscribe to this to get a collection of the current state of input
    def __init__(
        self,
        snapshot: InputSnapshot,
    ) -> None:
        self.snapshot = snapshot
        super().__init__()
