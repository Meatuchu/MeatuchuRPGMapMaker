# pyright: reportPrivateUsage=false
from typing import Set
from unittest.mock import MagicMock, call, patch
from pytest import raises
from MeatuchuRPGMapMaker.core_classes.window_manager import WindowManager, DEFAULT_WINDOW_NAME
from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.events import Event, NewThreadRequestEvent
from tests import VeryMagicMock


# tests
def test_construction() -> None:
    assert WindowManager()


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_window_already_exists(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = VeryMagicMock()
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
    mock_Tk.return_value = VeryMagicMock()
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


def test_create_window_requires_event_mgr() -> None:
    m = WindowManager()
    with raises(ValueError):
        m.create_window("pog")


def test_set_window_size_not_exist() -> None:
    m = WindowManager()
    with raises(KeyError):
        m.set_window_size(1, 2, "buckle my shoe")


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_create_window_thread_target(mock_tk: MagicMock) -> None:
    m = WindowManager()

    mock_event_mgr = MagicMock()
    event_types: Set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.name)
        if event.name == NewThreadRequestEvent.name:
            event.kwargs.get("thread_target")()

    mock_event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)

    m.register_event_mgr(mock_event_mgr)
    m.create_window("test")

    mock_event_mgr.queue_event.assert_called()
    assert NewThreadRequestEvent.name in event_types


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_set_fullscreen_mode_0(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = VeryMagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_mgr(event_mgr)
    w.create_window("side")
    w.create_window()
    w.set_fullscreen_mode(0, "side")
    w.set_fullscreen_mode(0)
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", False), call("-fullscreen", False)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_set_fullscreen_mode_1(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = VeryMagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_mgr(event_mgr)
    w.create_window("side")
    w.create_window()
    w.set_fullscreen_mode(1, "side")
    w.set_fullscreen_mode(1)
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", True), call("-fullscreen", True)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_set_fullscreen_mode_2(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = VeryMagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_mgr(event_mgr)
    w.create_window("side")
    w.create_window()
    w.set_fullscreen_mode(2, "side")
    w.set_fullscreen_mode(2)
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", True), call("-fullscreen", True)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_set_fullscreen_mode_not_exist(mock_tk: MagicMock) -> None:
    m = WindowManager()
    with raises(KeyError):
        m.set_fullscreen_mode(0, "test")
