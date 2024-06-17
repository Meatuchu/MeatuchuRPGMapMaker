# pyright: reportPrivateUsage=false
from unittest.mock import MagicMock

from pynput import keyboard, mouse

from MeatuchuRPGMapMaker.core_classes.input_manager import InputManager
from MeatuchuRPGMapMaker.events.Event import Event


def test_create_input_manager() -> None:
    InputManager()


def test_handle_keypress_key() -> None:
    m = InputManager()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    m.event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_keypress(keyboard.Key.space)
    assert m._pressed_keys["space"]
    assert "KeyPressEvent" in event_types


def test_handle_keypress_keycode() -> None:
    m = InputManager()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    m.event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_keypress(keyboard.KeyCode("vk", "f"))
    assert m._pressed_keys["f"]
    m.event_mgr.queue_event.assert_called()
    assert "KeyPressEvent" in event_types


def test_handle_keypress_no_key() -> None:
    m = InputManager()
    m.event_mgr.queue_event = MagicMock()
    m.handle_keypress(None)
    m.handle_keypress(keyboard.KeyCode())
    m.event_mgr.queue_event.assert_not_called()


def test_handle_keyrelease_key() -> None:
    m = InputManager()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    m.event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_keypress(keyboard.Key.space)
    m.handle_keyrelease(keyboard.Key.space)
    assert not m._pressed_keys.get("space")
    assert "KeyPressEvent" in event_types
    assert "KeyReleaseEvent" in event_types


def test_handle_keyrelease_keycode() -> None:
    m = InputManager()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    m.event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_keypress(keyboard.KeyCode("", "f"))
    m.handle_keyrelease(keyboard.KeyCode("", "f"))
    assert not m._pressed_keys.get("f")
    assert "KeyPressEvent" in event_types
    assert "KeyReleaseEvent" in event_types


def test_handle_keyrelease_no_key() -> None:
    m = InputManager()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    m.event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_keypress(keyboard.KeyCode())
    m.handle_keyrelease(keyboard.KeyCode())
    m.handle_keypress(None)
    m.handle_keyrelease(None)
    assert "KeyPressEvent" not in event_types
    assert "KeyReleaseEvent" not in event_types


def test_handle_mouse_move() -> None:
    m = InputManager()
    e = MagicMock()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)

    e.queue_event = MagicMock(side_effect=mock_queue_event)
    m.handle_mouse_move(0, 1)


def test_handle_mouse_click() -> None:
    m = InputManager()
    m.handle_mouse_click(0, 0, mouse.Button.left, True)
    m.handle_mouse_click(0, 0, mouse.Button.left, False)


def test_handle_mouse_scroll() -> None:
    m = InputManager()
    m.handle_mouse_scroll(0, 0, 1, 0)
    m.handle_mouse_scroll(0, 0, -1, 0)
