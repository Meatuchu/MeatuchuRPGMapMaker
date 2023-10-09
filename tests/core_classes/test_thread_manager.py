from unittest.mock import MagicMock, patch
from MeatuchuRPGMapMaker.core_classes.thread_manager import ThreadManager


def test_construction() -> None:
    assert ThreadManager()


def test_register_entity_manager() -> None:
    m = ThreadManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_mgr(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
