from typing import Any, Callable

from MeatuchuRPGMapMaker.events import AppShutDownEvent, Event

from ..Keybind import Keybind
from ..KeyState import KeyState


class CloseWindowKB(Keybind):
    def __init__(
        self, fire_event: Callable[[Event | dict[str, Any]], None], binds: list[dict[str, int]] | None = None
    ) -> None:
        if binds:
            self.states = [KeyState(bind) for bind in binds]
        else:
            self.states = [
                KeyState({"esc": 3000}),
                KeyState({"ctrl": 0, "w": 0}),
                KeyState({"ctrl_r": 0, "w": 0}),
                KeyState({"alt": 0, "f4": 0}),
                KeyState({"alt_r": 0, "f4": 0}),
            ]
        self.fire_event = fire_event
        super().__init__()

    def execute(self) -> None:
        self.fire_event(AppShutDownEvent())
