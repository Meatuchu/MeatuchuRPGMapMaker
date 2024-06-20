from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.events import (
    AllThreadsDestroyedEvent,
    AppShutDownEvent,
    CloseWindowEvent,
    DestroyThreadRequestEvent,
    Event,
    InputEvent,
    InputSnapshotEvent,
    KeyPressEvent,
    KeyReleaseEvent,
    LogEvent,
    MouseMoveEvent,
    NewThreadEvent,
    NewThreadRequestEvent,
    RenderEvent,
    SceneChangeEvent,
    SceneChangeRequestEvent,
    ThreadErrorEvent,
    UpdateEvent,
)


def test_event() -> None:
    assert Event
    assert Event()
    assert Event.from_dict({"name": "Event"})


def test_input_event() -> None:
    assert InputEvent
    assert InputEvent()
    assert InputEvent.from_dict({"name": "InputEvent"})


def test_update_event() -> None:
    assert UpdateEvent
    assert UpdateEvent()
    assert UpdateEvent.from_dict({"name": "UpdateEvent"})


def test_render_event() -> None:
    assert RenderEvent
    assert RenderEvent()
    assert RenderEvent.from_dict({"name": "RenderEvent"})


def test_new_thread_request_event() -> None:
    assert NewThreadRequestEvent
    assert NewThreadRequestEvent("test thread", MagicMock(), "unit_test")
    assert NewThreadRequestEvent.from_dict(
        {
            "name": "NewThreadRequestEvent",
            "thread_name": "test thread",
            "thread_target": MagicMock(),
            "owner_id": "unit_test",
        }
    )


def test_new_thread_event() -> None:
    assert NewThreadEvent
    assert NewThreadEvent("test thread")
    assert NewThreadEvent.from_dict({"name": "NewThreadEvent", "thread_name": "test thread"})


def test_destroy_thread_request_event() -> None:
    assert DestroyThreadRequestEvent
    assert DestroyThreadRequestEvent("test thread", "unit_test")
    assert DestroyThreadRequestEvent.from_dict(
        {
            "name": "DestroyThreadRequestEvent",
            "thread_name": "test thread",
            "owner_id": "unit_test",
        }
    )


def test_all_threads_destroyed_event() -> None:
    assert AllThreadsDestroyedEvent
    assert AllThreadsDestroyedEvent()
    assert AllThreadsDestroyedEvent.from_dict({"name": "AllThreadsDestroyedEvent"})


def test_close_window_event() -> None:
    assert CloseWindowEvent
    assert CloseWindowEvent()
    assert CloseWindowEvent.from_dict({"name": "CloseWindowEvent"})


def test_key_press_event() -> None:
    assert KeyPressEvent
    assert KeyPressEvent("esc")
    assert KeyPressEvent.from_dict({"name": "KeyPressEvent", "key": "esc"})


def test_key_release_event() -> None:
    assert KeyReleaseEvent
    assert KeyReleaseEvent("esc", 1)
    assert KeyReleaseEvent.from_dict({"name": "KeyReleaseEvent", "key": "esc", "hold_time": 1})


def test_mouse_move_event() -> None:
    assert MouseMoveEvent
    assert MouseMoveEvent(0, 1)
    assert MouseMoveEvent.from_dict({"name": "MouseMoveEvent", "x": 0, "y": 1})


def test_app_shutdown_event() -> None:
    assert AppShutDownEvent
    assert AppShutDownEvent()
    assert AppShutDownEvent.from_dict({"name": "AppShutDownEvent"})


def test_thread_error_event() -> None:
    assert ThreadErrorEvent
    assert ThreadErrorEvent("thread_name", "owner_id", Exception("test exception"))
    assert ThreadErrorEvent.from_dict(
        {
            "name": "ThreadErrorEvent",
            "thread_name": "thread_name",
            "owner_id": "owner_id",
            "exception": Exception("test exception"),
        }
    )


def test_scene_change_request_event() -> None:
    assert SceneChangeRequestEvent
    assert SceneChangeRequestEvent("MapEditScene")
    assert SceneChangeRequestEvent("MenuScene")
    assert SceneChangeRequestEvent("MapEditScene", "test_window", {"test": "value"})
    assert SceneChangeRequestEvent.from_dict(
        {
            "name": "SceneChangeRequestEvent",
            "scene_target": "MapEditScene",
            "window_name": "test_window",
            "scene_kwargs": {"test": "value"},
        }
    )


def test_scene_change_event() -> None:
    assert SceneChangeEvent
    assert SceneChangeEvent()
    assert SceneChangeEvent.from_dict({"name": "SceneChangeEvent"})


def test_log_event() -> None:
    assert LogEvent
    assert LogEvent("ERROR", "test message")
    assert LogEvent.from_dict({"name": "LogEvent", "msg_level": "ERROR", "msg": "test message"})


def test_input_snapshot_event() -> None:
    assert InputSnapshotEvent
    assert InputSnapshotEvent(InputSnapshot({"a": 123}, {}, (0, 0)))
    assert InputSnapshotEvent.from_dict(
        {"name": "InputSnapshotEvent", "snapshot": InputSnapshot({"a": 123}, {}, (0, 0))}
    )
