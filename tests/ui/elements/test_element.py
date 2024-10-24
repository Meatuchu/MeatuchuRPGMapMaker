from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.ui.elements.element import Element


def test_element_uuid() -> None:
    e = Element(MagicMock())
    assert type(e.uuid) is str
    assert len(e.uuid) == 36


def test_element_uuid_unique() -> None:
    e = Element(MagicMock())
    e2 = Element(MagicMock())
    assert e.uuid != e2.uuid
