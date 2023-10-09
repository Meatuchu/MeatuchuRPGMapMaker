# pyright: reportPrivateUsage=false
from typing import Any
from unittest.mock import MagicMock, call, patch
from pytest import raises
from MeatuchuRPGMapMaker.core_classes.window_manager import WindowManager, DEFAULT_WINDOW_NAME
from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager


# helper mock
class mock_tk_def:
    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except:
            super().__setattr__(__name, MagicMock())
            return super().__getattribute__(__name)

    def __init__(self) -> None:
        pass


# tests
def test_construction() -> None:
    assert WindowManager()


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_window_already_exists(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = mock_tk_def()
    w = WindowManager()
    o = w.create_window

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        o()
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_mgr(event_mgr)
    w.create_window()
    with raises(ValueError) as e:
        w.create_window()
    assert str(e.value) == f"Window {DEFAULT_WINDOW_NAME} already exists!"


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.NewThreadRequestEvent")
def test_window_activate(thread_request_event_def: MagicMock) -> None:
    w = WindowManager()
    event_mgr = EventManager()
    event_mgr.queue_event = MagicMock()
    w.register_event_mgr(event_mgr)
    w.create_window()
    w.create_window("side")
    event_mgr.queue_event.assert_has_calls(calls=[call(thread_request_event_def()), call(thread_request_event_def())])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_window_set_size(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = mock_tk_def()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_mgr(event_mgr)
    w.create_window("side")
    w.create_window()
    w.set_window_size(200, 200)
    w.set_window_size(300, 300, "side")
    mock_Tk.return_value.geometry.assert_has_calls([call("200x200"), call("300x300")])


def test_register_event_manager() -> None:
    m = WindowManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_mgr(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
