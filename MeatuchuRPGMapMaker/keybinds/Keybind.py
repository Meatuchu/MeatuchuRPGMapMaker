from typing import Callable, List

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.events import Event

from .KeyState import KeyState


class Keybind:
    states: List[KeyState]
    fire_event: Callable[[Event], None]
    __ready: bool

    def __init__(self) -> None:
        self.__ready = True
        try:
            assert self.states
            assert self.fire_event
        except (AssertionError, AttributeError):
            raise AttributeError("Keybinds must have a states list and a fire_event method")

    def check(self, input_snapshot: InputSnapshot) -> bool:
        try:
            self.__ready
        except AttributeError:
            raise AttributeError("Tried to check event which did not call parent contstructor")

        for state in self.states:
            if state.check(input_snapshot):
                self.execute()
                return True
        return False

    def execute(self) -> None:
        pass
