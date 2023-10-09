from typing import Optional, Union, Dict, Tuple
from pynput import keyboard, mouse
import time

from . import FeatureManager
from .event_manager import EventManager
from .events import KeyPressEvent, KeyReleaseEvent
from ..helpers import debounce


class InputManager(FeatureManager):
    event_mgr: EventManager
    key_listener: keyboard.Listener
    mouse_listener: mouse.Listener
    _pressed_keys: Dict[str, int]
    _pressed_mouse_buttons: Dict[str, Tuple[int, int]]
    _last_mouse_pos_log_time: int = 0

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

    def register_event_mgr(self, event_mgr: EventManager) -> None:
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

        if self._pressed_keys.get(c):
            t = self._pressed_keys.pop(c)
            hold_time_ms = (time.time_ns() - t) / 1000000
            self.event_mgr.queue_event(KeyReleaseEvent(c, hold_time_ms))

    @debounce(1)
    def _mouse_move_log(self, x: int, y: int) -> None:
        self.log("DEBUG", f"Mouse Move Event at {x}, {y}")

    def handle_mouse_move(self, x: int, y: int) -> None:
        self._mouse_move_log(x, y)
        pass

    def handle_mouse_click(
        self,
        x: int,
        y: int,
        button: mouse.Button,
        pressed: bool,
    ) -> None:
        self.log("DEBUG", f"mouse {button.name} click event at {x}, {y} ({pressed})")
        pass

    def handle_mouse_scroll(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
    ) -> None:
        self.log("DEBUG", f"mouse scroll event at {x}, {y} ({dx}, {dy})")
        pass
