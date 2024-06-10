from unittest.mock import MagicMock, call, patch

from pytest import raises

from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.window_manager import (
    DEFAULT_WINDOW_NAME,
    WindowManager,
)
from MeatuchuRPGMapMaker.events.Event import Event
from MeatuchuRPGMapMaker.events.NewThreadRequestEvent import NewThreadRequestEvent
from MeatuchuRPGMapMaker.events.RenderEvent import RenderEvent
from MeatuchuRPGMapMaker.events.SceneChangeRequestEvent import SceneChangeRequestEvent
from MeatuchuRPGMapMaker.events.WindowFullscreenModeEditRequestEvent import (
    WindowFullscreenModeEditRequestEvent,
)
from MeatuchuRPGMapMaker.events.WindowResizeRequestEvent import WindowResizeRequestEvent
from MeatuchuRPGMapMaker.exceptions import (
    DuplicateWindowError,
    WindowNotExistError,
    WindowNotFoundError,
)
from MeatuchuRPGMapMaker.ui.scenes.scene import Scene

# pyright: reportPrivateUsage=false

WindowManager.window_create_timeout = 0.1


# tests
def test_construction() -> None:
    assert WindowManager()


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_window_already_exists(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = MagicMock()
    w = WindowManager()
    o = w.create_window

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        o()
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)
    w.create_window()
    with raises(DuplicateWindowError) as e:
        w.create_window()
    assert str(e.value) == f"Window {DEFAULT_WINDOW_NAME} already exists!"


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.NewThreadRequestEvent")
def test_window_activate(thread_request_event_def: MagicMock) -> None:
    w = WindowManager()
    event_mgr = EventManager()
    event_mgr.queue_event = MagicMock()
    w.register_event_manager(event_mgr)
    w.create_window()
    w.create_window("side")
    event_mgr.queue_event.assert_has_calls(calls=[call(thread_request_event_def()), call(thread_request_event_def())])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_window_set_size(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = MagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    set_size_event_1 = WindowResizeRequestEvent(200, 200)
    set_size_event_2 = WindowResizeRequestEvent(300, 300, "side")
    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)
    w.create_window("side")
    w.create_window()
    w.set_window_size(set_size_event_1)
    w.set_window_size(set_size_event_2)
    mock_Tk.return_value.geometry.assert_has_calls([call("200x200"), call("300x300")])


def test_register_event_manager() -> None:
    m = WindowManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_manager(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()


def test_set_window_size_not_exist() -> None:
    m = WindowManager()
    set_size_event = WindowResizeRequestEvent(1, 2, "buckle_my_shoe")
    with raises(WindowNotExistError):
        m.set_window_size(set_size_event)


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_create_window_thread_target(mock_tk: MagicMock) -> None:
    m = WindowManager()
    m._get_window_thread = MagicMock()

    mock_event_mgr = MagicMock()
    event_types: set[str] = set()

    def mock_queue_event(event: Event) -> None:
        nonlocal event_types
        event_types.add(event.__class__.__name__)
        if isinstance(event, NewThreadRequestEvent):
            event.thread_target()

    mock_event_mgr.queue_event = MagicMock(side_effect=mock_queue_event)

    m.register_event_manager(mock_event_mgr)
    m.create_window("test")

    mock_event_mgr.queue_event.assert_called()
    assert NewThreadRequestEvent.__name__ in event_types


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_set_fullscreen_mode_0(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = MagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)
    w.create_window("side")
    w.create_window()
    mode = 0
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode, "side"))
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode))
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", False), call("-fullscreen", False)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_set_fullscreen_mode_1(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = MagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)
    w.create_window("side")
    w.create_window()
    mode = 1
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode, "side"))
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode))
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", True), call("-fullscreen", True)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_set_fullscreen_mode_2(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = MagicMock()
    w = WindowManager()

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        w._windows[window_name] = mock_Tk()
        w._canvases[window_name] = mock_Tk()

    w.create_window = _new_window_thread_mock
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)
    w.create_window("side")
    w.create_window()
    mode = 2
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode, "side"))
    w.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode))
    mock_Tk.return_value.attributes.assert_has_calls([call("-fullscreen", True), call("-fullscreen", True)])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_set_fullscreen_mode_not_exist(mock_tk: MagicMock) -> None:
    m = WindowManager()
    with raises(WindowNotExistError):
        m.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(0, "buckle_my_shoe"))


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_pass_event_to_window_queue_name_empty(mock_tk: MagicMock) -> None:
    w = WindowManager()

    window_name = "main"

    event1 = MagicMock(spec=RenderEvent)
    event2 = MagicMock(spec=RenderEvent)
    event1.window_name = None
    event2.window_name = ""

    # Test when window exists
    w._windows[window_name] = MagicMock()
    w.pass_event_to_window_queue(event1)
    assert len(w._window_events[window_name]) == 1
    assert w._window_events[window_name][0] == event1

    # Test when window does not exist
    w._windows[window_name] = None
    w.pass_event_to_window_queue(event2)
    assert len(w._window_events[window_name]) == 2
    assert w._window_events[window_name][1] == event2


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
def test_pass_event_to_window_queue_named(mock_tk: MagicMock) -> None:
    w = WindowManager()

    window_name = "some_other_window"

    event1 = MagicMock(spec=RenderEvent)
    event2 = MagicMock(spec=RenderEvent)
    event1.window_name = window_name
    event2.window_name = window_name

    # Test when window exists
    w._windows[window_name] = MagicMock()
    w.pass_event_to_window_queue(event1)
    assert len(w._window_events[window_name]) == 1
    assert w._window_events[window_name][0] == event1

    # Test when window does not exist
    w._windows[window_name] = None
    w.pass_event_to_window_queue(event2)
    assert len(w._window_events[window_name]) == 2
    assert w._window_events[window_name][1] == event2


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
@patch("MeatuchuRPGMapMaker.core_classes.window_manager.SceneChangeEvent")
def test_load_scene(
    mock_scene_change_event: MagicMock,
    mock_tk: MagicMock,
) -> None:
    # Mock SceneChangeEvent
    mock_scene_change_event.return_value = MagicMock()

    # Create window manager
    w = WindowManager()
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)

    # Mock create_window
    o = w.create_window

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        o()
        w._windows[window_name] = mock_tk()
        w._canvases[window_name] = mock_tk()

    w.create_window = _new_window_thread_mock

    # Prepare window
    w.create_window()
    event_mgr.queue_event = MagicMock()

    # Test
    w.load_scene(SceneChangeRequestEvent("MapEditScene"))
    event_mgr.queue_event.assert_called_once_with(mock_scene_change_event.return_value)


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.TkWindow")
@patch("MeatuchuRPGMapMaker.core_classes.window_manager.SceneChangeEvent")
def test_load_new_scene(
    mock_scene_change_event: MagicMock,
    mock_tk: MagicMock,
) -> None:
    mock_scene_def = MagicMock(spec=Scene, __name__="Scene")
    # Mock SceneChangeEvent
    old_scene = MagicMock(spec=Scene, unload=MagicMock())
    old_scene.name = "OldScene"
    new_scene = MagicMock(spec=Scene, unload=MagicMock())
    new_scene.name = "NewScene"

    mock_scene_change_event.return_value = MagicMock()

    # Create window manager
    w = WindowManager()
    event_mgr = EventManager()
    w.register_event_manager(event_mgr)

    # Mock create_window
    o = w.create_window

    def _new_window_thread_mock(window_name: str = DEFAULT_WINDOW_NAME) -> None:
        o()
        w._windows[window_name] = mock_tk()
        w._canvases[window_name] = mock_tk()

    w.create_window = _new_window_thread_mock

    # Prepare window
    w.create_window()
    event_mgr.queue_event = MagicMock()

    # Test
    event1 = SceneChangeRequestEvent("MapEditScene")
    mock_scene_def.return_value = old_scene
    event1.scene_to_load = mock_scene_def  # pyright: ignore[reportAttributeAccessIssue]
    w.load_scene(event1)
    assert w._scenes[DEFAULT_WINDOW_NAME] == old_scene

    event2 = SceneChangeRequestEvent("MapEditScene")
    mock_scene_def.return_value = new_scene
    event2.scene_to_load = mock_scene_def  # pyright: ignore[reportAttributeAccessIssue]
    w.load_scene(event2)
    old_scene.unload.assert_called_once()
    assert w._scenes[DEFAULT_WINDOW_NAME] == new_scene


def test_wait_for_window_fail() -> None:
    m = WindowManager()
    m.window_create_timeout = 0.01
    m._windows = {"buckle_my_shoe": None}
    with raises(WindowNotFoundError):
        m._wait_for_window("buckle_my_shoe")


def test_wait_for_window_not_exist() -> None:
    m = WindowManager()
    with raises(WindowNotExistError):
        m._wait_for_window("buckle_my_shoe")


def test_render_step_with_outgoing_events() -> None:
    # Create a mock event manager
    event_mgr = MagicMock()

    # Create a mock event
    event = MagicMock(spec=Event)

    # Create a mock window manager
    w = WindowManager()
    w.event_mgr = event_mgr
    w._outgoing_events = [event]

    # Call the render_step method
    w.render_step(1)

    # Assert that the event manager's queue_event method was called with the event
    event_mgr.queue_event.assert_called_once_with(event)


def test_render_step_without_outgoing_events() -> None:
    # Create a mock event manager
    event_mgr = MagicMock()

    # Create a mock window manager
    w = WindowManager()
    w.event_mgr = event_mgr
    w._outgoing_events = []

    # Call the render_step method
    w.render_step(1)

    # Assert that the event manager's queue_event method was not called
    event_mgr.queue_event.assert_not_called()
