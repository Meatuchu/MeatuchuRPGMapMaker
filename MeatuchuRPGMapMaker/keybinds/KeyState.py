import time
from typing import Dict

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.constants import NS_PER_MS

MODIFIER_KEYS = ["ctrl", "ctrl_r", "alt", "alt_r", "shift", "shift_r"]


class KeyState:
    allow_hold_refire: bool
    __is_fired: bool

    def __init__(self, keys: Dict[str, int], allow_hold_refire: bool = False, modifiers_first: bool = True) -> None:
        for key in keys:
            if keys[key] < 0:
                raise ValueError("Keybinds must have a hold requirement of at least 0 ns")

        self.allow_hold_refire = allow_hold_refire
        self.modifiers_first = modifiers_first
        self.keys = keys
        self.__is_fired = False

    def check(self, input_snapshot: InputSnapshot) -> bool:
        # Get the lowest timestamp of all non-modifier keys - if none are required for the bind, set to infinity
        lowest_non_modifier_timestamp = min(
            [input_snapshot.keys.get(key, 0) for key in self.keys if key not in MODIFIER_KEYS],
            default=float("inf"),
        )

        # If no non-modifier keys are pressed and the bind requires one, the keybind is not ready to fire
        if lowest_non_modifier_timestamp == 0:
            self.__is_fired = False
            return False

        for key, hold_requirement in self.keys.items():
            if (
                not (
                    input_snapshot.keys.get(key)
                    and input_snapshot.keys[key] + (hold_requirement * NS_PER_MS) < time.time_ns()
                )
            ) or (
                self.modifiers_first
                and key in MODIFIER_KEYS
                and input_snapshot.keys[key] > lowest_non_modifier_timestamp
            ):
                self.__is_fired = False
                return False

        if (not self.allow_hold_refire) and self.__is_fired:
            return False

        self.__is_fired = True
        return True

    def get_is_fired(self) -> bool:
        return self.__is_fired
