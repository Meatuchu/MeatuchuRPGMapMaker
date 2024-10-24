from unittest.mock import MagicMock

from pytest import raises

from MeatuchuRPGMapMaker.ui.elements.root import Root


def test_root_parse_main_menu() -> None:
    root = Root(MagicMock(), "main_menu")
    root.parse()


def test_root_debug_namespace() -> None:
    root = Root(MagicMock(), "valid", "debug")
    root.parse()


def test_root_duplicate_id() -> None:
    root = Root(MagicMock(), "duplicate_id", "debug")
    with raises(ValueError):
        root.parse()


def test_root_invalid_children() -> None:
    root = Root(MagicMock(), "invalid_children", "debug")
    with raises(ValueError):
        root.parse()
