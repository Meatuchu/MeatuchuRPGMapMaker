from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes import events


def test_event() -> None:
    assert events.Event
    assert events.Event()


def test_input_event() -> None:
    assert events.InputEvent
    assert events.InputEvent()


def test_update_event() -> None:
    assert events.UpdateEvent
    assert events.UpdateEvent()


def test_render_event() -> None:
    assert events.RenderEvent
    assert events.RenderEvent()


def test_new_thread_request_event() -> None:
    assert events.NewThreadRequestEvent
    assert events.NewThreadRequestEvent("test thread", MagicMock(), "unit_test")


def test_new_thread_event() -> None:
    assert events.NewThreadEvent
    assert events.NewThreadEvent("test thread")


def test_destroy_thread_request_event() -> None:
    assert events.DestroyThreadRequestEvent
    assert events.DestroyThreadRequestEvent("test thread", "unit_test")


def test_all_threads_destroyed_event() -> None:
    assert events.AllThreadsDestroyedEvent
    assert events.AllThreadsDestroyedEvent()


def test_close_window_event() -> None:
    assert events.CloseWindowEvent
    assert events.CloseWindowEvent()


def test_key_press_event() -> None:
    assert events.KeyPressEvent
    assert events.KeyPressEvent("esc")


def test_key_release_event() -> None:
    assert events.KeyReleaseEvent
    assert events.KeyReleaseEvent("esc", 1)


def test_mouse_move_event() -> None:
    assert events.MouseMoveEvent
    assert events.MouseMoveEvent(0, 1)


def test_app_shutdown_event() -> None:
    assert events.AppShutDownEvent
    assert events.AppShutDownEvent()
