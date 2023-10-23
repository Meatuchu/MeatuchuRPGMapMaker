from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes.ui_manager import UIManager


def test_construction() -> None:
    assert UIManager()


def test_register_event_manager() -> None:
    UIManager().register_event_manager(MagicMock())
