import time
from typing import Dict, Optional, Tuple, Union, cast

from pynput import keyboard, mouse

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.constants import NS_PER_MS
from MeatuchuRPGMapMaker.events import (
    InputSnapshotEvent,
    KeyPressEvent,
    KeyReleaseEvent,
    MouseClickEvent,
    MouseClickReleaseEvent,
    MouseMoveEvent,
    MouseScrollEvent,
)
from MeatuchuRPGMapMaker.helpers import debounce

from . import FeatureManager
from .event_manager import EventManager


class InputManager(FeatureManager):
    event_mgr: EventManager
    key_listener: keyboard.Listener
    mouse_listener: mouse.Listener
    _pressed_keys: Dict[str, int]
    _pressed_mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]]
    _mouse_position: Tuple[int, int]

    def __init__(self) -> None:
        super().__init__()
        self.key_listener = keyboard.Listener(
            on_press=self.handle_keypress,
            on_release=self.handle_keyrelease,
        )
        self.key_listener.start()
        self.log("DEBUG", "Initiated key listener")
        self.mouse_listener = mouse.Listener(
            on_move=self.handle_mouse_move,
            on_click=self.handle_mouse_click,
            on_scroll=self.handle_mouse_scroll,
        )
        self.mouse_listener.start()
        self.log("DEBUG", "Initiated Mouse Listener")
        self._pressed_keys = {}
        self._pressed_mouse_buttons = {}
        self._mouse_position = (0, 0)

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass

    def handle_keypress(
        self,
        key: Optional[Union[keyboard.KeyCode, keyboard.Key]],
    ) -> None:
        if not key:
            return
        c = ""
        if isinstance(key, keyboard.KeyCode):
            c = key.char
        if isinstance(key, keyboard.Key):
            c = key.name
        if not c:
            return

        c = c.lower()

        if not self._pressed_keys.get(c):
            self._pressed_keys[c] = time.time_ns()
            self.event_mgr.queue_event(KeyPressEvent(c))

    def handle_keyrelease(
        self,
        key: Optional[Union[keyboard.KeyCode, keyboard.Key]],
    ) -> None:
        if not key:
            return
        c = ""
        if isinstance(key, keyboard.KeyCode):
            c = key.char
        if isinstance(key, keyboard.Key):
            c = key.name

        if not c:
            return

        c = c.lower()

        if self._pressed_keys.get(c):
            t = self._pressed_keys.pop(c)
            hold_time_ms = (time.time_ns() - t) / NS_PER_MS
            self.event_mgr.queue_event(KeyReleaseEvent(c, hold_time_ms))
        else:
            self.log("ERROR", f"Detected key release for non-pressed key {c}")

    @debounce(1)
    def _mouse_move_log(self, x: int, y: int) -> None:
        self.log("VERBOSE", f"Mouse Move Event at {x}, {y}")

    def handle_mouse_move(self, x: int, y: int) -> None:
        self._mouse_move_log(x, y)
        self._mouse_position = (x, y)
        self.event_mgr.queue_event(MouseMoveEvent(x=x, y=y))

    def handle_mouse_click(
        self,
        x: int,
        y: int,
        button: mouse.Button,
        pressed: bool,
    ) -> None:
        if pressed:
            # this is a click event
            if not self._pressed_mouse_buttons.get(button.name):
                self._pressed_mouse_buttons[button.name] = {"press_time": time.time_ns(), "position": (x, y)}
                self.event_mgr.queue_event(MouseClickEvent(button.name, (x, y)))
            else:
                self.log("ERROR", f"Detected click for pressed mouse button {button.name}")
        else:
            # this is a release event
            if self._pressed_mouse_buttons.get(button.name):
                t = self._pressed_mouse_buttons.pop(button.name)
                click_time_ms = (time.time_ns() - cast(int, t["press_time"])) / NS_PER_MS
                self.event_mgr.queue_event(MouseClickReleaseEvent(button.name, (x, y), click_time_ms))
            else:
                self.log("ERROR", f"Detected click release for non-pressed mouse button {button.name}")

    def handle_mouse_scroll(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
    ) -> None:
        self.event_mgr.queue_event(MouseScrollEvent(x, y, dx, dy))

    def input_step(self, frame_number: int) -> None:
        self.event_mgr.queue_event(
            InputSnapshotEvent(
                InputSnapshot(
                    self._pressed_keys,
                    self._pressed_mouse_buttons,
                    self._mouse_position,
                )
            )
        )
        return super().input_step(frame_number)
