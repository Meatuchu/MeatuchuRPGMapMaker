from typing import Callable, Dict, List, Optional

from MeatuchuRPGMapMaker.events import AppShutDownEvent, Event

from ..Keybind import Keybind
from ..KeyState import KeyState


class CloseWindowKB(Keybind):
    def __init__(self, fire_event: Callable[[Event], None], binds: Optional[List[Dict[str, int]]] = None) -> None:
        if binds:
            self.states = [KeyState(bind) for bind in binds]
        else:
            self.states = [
                KeyState({"esc": 1000}),
                KeyState({"ctrl": 0, "w": 0}),
                KeyState({"alt": 0, "f4": 0}),
            ]
        self.fire_event = fire_event
        super().__init__()

    def execute(self) -> None:
        self.fire_event(AppShutDownEvent())
        pass
