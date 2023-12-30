from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.ui.elements.primitive_elements.base_element import Element


def test_construction() -> None:
    assert Element(MagicMock(), "testelement")
