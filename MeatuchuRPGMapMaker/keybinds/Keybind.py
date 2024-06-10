from typing import Callable

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.events import Event, LogEvent

from .KeyState import KeyState


class Keybind:
    states: list[KeyState]
    fire_event: Callable[[Event], None]
    __ready: bool

    def __init__(self) -> None:
        self.__ready = True
        try:
            assert self.states
            assert self.fire_event
        except (AssertionError, AttributeError):
            raise AttributeError(f"{self.__class__.__name__} must have a states list and a fire_event method")
        self.fire_event(LogEvent("VERBOSE", f"Keybind {self.__class__.__name__} ready"))

    def check(self, input_snapshot: InputSnapshot) -> bool:
        try:
            self.__ready
        except AttributeError:
            raise AttributeError(
                f"Tried to check KeyBind {self.__class__.__name__} which did not call parent contstructor"
            )

        for state in self.states:
            if state.check(input_snapshot):
                self.fire_event(LogEvent("VERBOSE", f"Keybind {self.__class__.__name__} triggered"))
                self.execute()
                return True
        return False

    def execute(self) -> None:
        pass
