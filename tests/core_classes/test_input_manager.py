# pyright: reportPrivateUsage=false
from typing import Set
from unittest.mock import MagicMock

from pynput import keyboard, mouse

from MeatuchuRPGMapMaker.core_classes.events import Event
from MeatuchuRPGMapMaker.core_classes.input_manager import InputManager


def test_create_input_manager() -> None:
    InputManager()


def test_register_event_manager() -> None:
    m = InputManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_manager(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()


def test_handle_keypress_key() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_keypress(keyboard.Key.space)
    assert m._pressed_keys["space"]
    assert "KeyPressEvent" in event_types


def test_handle_keypress_keycode() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_keypress(keyboard.KeyCode("vk", "f"))
    assert m._pressed_keys["f"]
    e.queue_event.assert_called()
    assert "KeyPressEvent" in event_types


def test_handle_keypress_no_key() -> None:
    m = InputManager()
    e = MagicMock()
    e.queue_event = MagicMock()
    m.register_event_manager(e)
    m.handle_keypress(None)
    m.handle_keypress(keyboard.KeyCode())
    e.queue_event.assert_not_called()


def test_handle_keyrelease_key() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_keypress(keyboard.Key.space)
    m.handle_keyrelease(keyboard.Key.space)
    assert not m._pressed_keys.get("space")
    assert "KeyPressEvent" in event_types
    assert "KeyReleaseEvent" in event_types


def test_handle_keyrelease_keycode() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_keypress(keyboard.KeyCode("", "f"))
    m.handle_keyrelease(keyboard.KeyCode("", "f"))
    assert not m._pressed_keys.get("f")
    assert "KeyPressEvent" in event_types
    assert "KeyReleaseEvent" in event_types


def test_handle_keyrelease_no_key() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_keypress(keyboard.KeyCode())
    m.handle_keyrelease(keyboard.KeyCode())
    m.handle_keypress(None)
    m.handle_keyrelease(None)
    assert "KeyPressEvent" not in event_types
    assert "KeyReleaseEvent" not in event_types


def test_handle_mouse_move() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.register_event_manager(e)
    m.handle_mouse_move(0, 1)


def test_handle_mouse_click() -> None:
    m = InputManager()
    m.register_event_manager(MagicMock())
    m.handle_mouse_click(0, 0, mouse.Button.left, True)
    m.handle_mouse_click(0, 0, mouse.Button.left, False)


def test_handle_mouse_scroll() -> None:
    m = InputManager()
    m.register_event_manager(MagicMock())
    m.handle_mouse_scroll(0, 0, 1, 0)
    m.handle_mouse_scroll(0, 0, -1, 0)
