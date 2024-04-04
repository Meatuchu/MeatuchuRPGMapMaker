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


@patch("MeatuchuRPGMapMaker.core_classes.event_manager.time.time")
def test_schedule_event(mock_time: MagicMock) -> None:
    mock_time.return_value = 0
    e = EventManager()
    event1 = Event()
    event2 = Event()
    event3 = Event()
    e.schedule_event(event1, 100)
    e.schedule_event(event2, 100)
    e.schedule_event(event3, 50)
    assert e._scheduled_events.peekitem(0) == (50, [event3])  # type: ignore
    assert e._scheduled_events.peekitem(1) == (100, [event1, event2])  # type: ignore
    assert e._scheduled_events.popitem(0) == (50, [event3])  # type: ignore
    assert e._scheduled_events.popitem(0) == (100, [event1, event2])  # type: ignore


@patch("MeatuchuRPGMapMaker.core_classes.event_manager.time.time")
def test_schedule_event_queued(mock_time: MagicMock) -> None:
    # Set reference time
    mock_time.return_value = 0

    # Create EventManager
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(Event, trigger_func)

    event1 = Event()
    event2 = Event()
    event3 = Event()
    e.schedule_event(event1, 100)
    e.schedule_event(event2, 100)
    e.schedule_event(event3, 50)

    # Simulate time passing
    mock_time.return_value = 51

    # Process scheduled events
    e.queue_scheduled_events()
    e.input_step(0)

    # Check that the events were triggered
    assert e._scheduled_events.peekitem(0) == (100, [event1, event2])  # type: ignore
    trigger_func.assert_has_calls(calls=[call(event3)])

    # Simulate time passing
    mock_time.return_value = 101

    e.queue_scheduled_events()
    e.input_step(0)

    assert not e._scheduled_events  # type: ignore
    trigger_func.assert_has_calls(
        calls=[call(event1), call(event2)],
    )
