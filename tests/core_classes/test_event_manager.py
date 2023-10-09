from unittest.mock import MagicMock, call, patch
from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.events import Event, AppShutDownEvent


class MockEvent(Event):
    name: str = "MockEvent"


def test_construction() -> None:
    assert EventManager()


def test_register_subscription() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(MockEvent, trigger_func)


def test_queue_event() -> None:
    e = EventManager()
    e.queue_event(MockEvent())


def test_process_next_event() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(MockEvent, trigger_func)
    e.queue_event(MockEvent())
    e.process_next_event()
    trigger_func.assert_called_once()


def test_process_all_events() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(MockEvent, trigger_func)
    e.queue_event(MockEvent())
    e.queue_event(MockEvent())
    e.queue_event(MockEvent())
    e.process_all_events()
    trigger_func.assert_has_calls(calls=[call(), call(), call()])


def test_process_all_events_empty_queue() -> None:
    e = EventManager()
    trigger_func = MagicMock()
    e.register_subscription(MockEvent, trigger_func)
    e.process_all_events()
    trigger_func.assert_not_called()


@patch("MeatuchuRPGMapMaker.core_classes.event_manager.sys.exit")
def test_app_shutdown_event(mock_sys_exit: MagicMock) -> None:
    e = EventManager()
    e.queue_event(AppShutDownEvent())
    e.process_all_events()
    mock_sys_exit.assert_called_once()
