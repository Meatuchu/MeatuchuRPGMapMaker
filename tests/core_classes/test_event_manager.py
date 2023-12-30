from unittest.mock import MagicMock, call, patch
from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.events import Event, InputEvent, UpdateEvent, RenderEvent, AppShutDownEvent


def test_construction() -> None:
    assert EventManager()


def test_register_subscription() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)


def test_queue_event() -> None:
    e = EventManager()
    e.queue_event(Event())


def test_process_next_event() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)
    e.queue_event(Event())
    e.process_next_event(None)
    trigger_func.assert_called_once()


def test_process_all_input_events() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)
    e1 = InputEvent()
    e2 = InputEvent()
    e3 = InputEvent()
    e.queue_event(e1)
    e.queue_event(e2)
    e.queue_event(e3)
    e.input_step(0)
    trigger_func.assert_has_calls(calls=[call(e1), call(e2), call(e3)])


def test_process_all_update_events() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)
    e1 = UpdateEvent()
    e2 = UpdateEvent()
    e3 = UpdateEvent()
    e.queue_event(e1)
    e.queue_event(e2)
    e.queue_event(e3)
    e.update_step(0)
    trigger_func.assert_has_calls(calls=[call(e1), call(e2), call(e3)])


def test_process_all_render_events() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)
    e2 = RenderEvent()
    e1 = RenderEvent()
    e3 = RenderEvent()
    e.queue_event(e1)
    e.queue_event(e2)
    e.queue_event(e3)
    e.render_step(0)
    trigger_func.assert_has_calls(calls=[call(e1), call(e2), call(e3)])


def test_process_all_events_empty_queue() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)
    e.input_step(0)
    e.update_step(0)
    e.render_step(0)
    trigger_func.assert_not_called()


@patch("MeatuchuRPGMapMaker.core_classes.event_manager.sys.exit")
def test_app_shutdown_event(mock_sys_exit: MagicMock) -> None:
    e = EventManager()
    e.queue_event(AppShutDownEvent())
    e.input_step(0)
    e.update_step(0)
    e.render_step(0)
    mock_sys_exit.assert_called_once()
