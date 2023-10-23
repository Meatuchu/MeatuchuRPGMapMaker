from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes.export_manager import ExportManager


def test_create_export_manager() -> None:
    ExportManager()


def test_register_event_manager() -> None:
    m = ExportManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_manager(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
