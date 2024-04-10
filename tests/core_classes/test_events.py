from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import (
    AllThreadsDestroyedEvent,
    AppShutDownEvent,
    CloseWindowEvent,
    DestroyThreadRequestEvent,
    Event,
    InputEvent,
    KeyPressEvent,
    KeyReleaseEvent,
    MouseMoveEvent,
    NewThreadEvent,
    NewThreadRequestEvent,
    RenderEvent,
    UpdateEvent,
)


def test_event() -> None:
    assert Event
    assert Event()


def test_input_event() -> None:
    assert InputEvent
    assert InputEvent()


def test_update_event() -> None:
    assert UpdateEvent
    assert UpdateEvent()


def test_render_event() -> None:
    assert RenderEvent
    assert RenderEvent()


def test_new_thread_request_event() -> None:
    assert NewThreadRequestEvent
    assert NewThreadRequestEvent("test thread", MagicMock(), "unit_test")


def test_new_thread_event() -> None:
    assert NewThreadEvent
    assert NewThreadEvent("test thread")


def test_destroy_thread_request_event() -> None:
    assert DestroyThreadRequestEvent
    assert DestroyThreadRequestEvent("test thread", "unit_test")


def test_all_threads_destroyed_event() -> None:
    assert AllThreadsDestroyedEvent
    assert AllThreadsDestroyedEvent()


def test_close_window_event() -> None:
    assert CloseWindowEvent
    assert CloseWindowEvent()


def test_key_press_event() -> None:
    assert KeyPressEvent
    assert KeyPressEvent("esc")


def test_key_release_event() -> None:
    assert KeyReleaseEvent
    assert KeyReleaseEvent("esc", 1)


def test_mouse_move_event() -> None:
    assert MouseMoveEvent
    assert MouseMoveEvent(0, 1)


def test_app_shutdown_event() -> None:
    assert AppShutDownEvent
    assert AppShutDownEvent()
