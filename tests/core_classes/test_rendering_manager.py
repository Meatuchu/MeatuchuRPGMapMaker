from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes.rendering_manager import RenderingManager


def test_create_rendering_manager() -> None:
    RenderingManager()


def test_register_event_manager() -> None:
    m = RenderingManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_mgr(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
