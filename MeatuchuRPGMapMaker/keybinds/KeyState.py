import time
from typing import Dict

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.constants import NS_PER_MS


class KeyState:
    allow_hold_refire: bool
    __fired: bool

    def __init__(self, keys: Dict[str, int], allow_hold_refire: bool = False) -> None:
        for key in keys:
            if keys[key] < 0:
                raise ValueError("Keybinds must have a hold requirement of at least 0 ns")

        self.allow_hold_refire = allow_hold_refire
        self.keys = keys
        self.__fired = False

    def check(self, input_snapshot: InputSnapshot) -> bool:
        for key, hold_requirement in self.keys.items():
            if not (
                input_snapshot.keys.get(key)
                and input_snapshot.keys[key] + (hold_requirement * NS_PER_MS) < time.time_ns()
            ):
                self.__fired = False
                return False

        if (not self.allow_hold_refire) and self.__fired:
            return False

        self.__fired = True
        return True
