from typing import Callable, Dict, List, Optional

from MeatuchuRPGMapMaker.events import (
    Event,
    WindowFullscreenModeEditRequestEvent,
)

from ..Keybind import Keybind
from ..KeyState import KeyState


class FullScreenKB(Keybind):
    def __init__(self, fire_event: Callable[[Event], None], binds: Optional[List[Dict[str, int]]] = None) -> None:
        if binds:
            self.states = [KeyState(bind) for bind in binds]
        else:
            self.states = [
                KeyState({"f11": 0}),
            ]
        self.fire_event = fire_event
        super().__init__()

    def execute(self) -> None:
        self.fire_event(WindowFullscreenModeEditRequestEvent(2))
        pass