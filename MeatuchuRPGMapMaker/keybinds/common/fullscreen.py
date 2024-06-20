from typing import Callable

from MeatuchuRPGMapMaker.events import (
    EventQueueItemType,
    WindowToggleFullscreenModeRequestEvent,
)

from ..Keybind import Keybind
from ..KeyState import KeyState


class FullScreenKB(Keybind):
    def __init__(
        self, fire_event: Callable[[EventQueueItemType], None], binds: list[dict[str, int]] | None = None
    ) -> None:
        if binds:
            self.states = [KeyState(bind) for bind in binds]
        else:
            self.states = [
                KeyState({"f11": 0}),
                KeyState({"alt": 1, "enter": 0}),
                KeyState({"alt_r": 1, "enter": 0}),
            ]
        self.fire_event = fire_event
        super().__init__()

    def execute(self) -> None:
        self.fire_event(WindowToggleFullscreenModeRequestEvent())
