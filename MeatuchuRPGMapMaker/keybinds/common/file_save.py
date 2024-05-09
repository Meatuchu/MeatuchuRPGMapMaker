from typing import Callable, Dict, List, Optional

from MeatuchuRPGMapMaker.events import Event, FileSaveRequestEvent

from ..Keybind import Keybind
from ..KeyState import KeyState


class FileSaveKB(Keybind):
    def __init__(self, fire_event: Callable[[Event], None], binds: Optional[List[Dict[str, int]]] = None) -> None:
        if binds:
            self.states = [KeyState(bind) for bind in binds]
        else:
            self.states = [
                KeyState({"ctrl": 0, "s": 0}),
                KeyState({"ctrl_r": 0, "s": 0}),
            ]
        self.fire_event = fire_event
        super().__init__()

    def execute(self) -> None:
        self.fire_event(FileSaveRequestEvent())
        pass
