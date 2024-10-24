from pytest import raises

from MeatuchuRPGMapMaker.ui.types import Margin, Padding


def test_margin_int_construction() -> None:
    m = Margin(12)
    assert m.left == 12
    assert m.right == 12
    assert m.top == 12
    assert m.bottom == 12


def test_margin_dict_construction() -> None:
    m = Margin({"top": 12, "bottom": 0, "left": 3, "right": 4})
    assert m.left == 3
    assert m.right == 4
    assert m.top == 12
    assert m.bottom == 0


def test_margin_dict_construction_incomplete() -> None:
    m = Margin({"top": 12})
    assert m.top == 12
    assert m.left == 0
    assert m.right == 0
    assert m.bottom == 0


def test_margin_negative_values() -> None:
    with raises(ValueError):
        Margin(-1)
    with raises(ValueError):
        Margin({"top": -1})


def test_padding_int_construction() -> None:
    m = Padding(12)
    assert m.left == 12
    assert m.right == 12
    assert m.top == 12
    assert m.bottom == 12


def test_padding_dict_construction() -> None:
    m = Padding({"top": 12, "bottom": 0, "left": 3, "right": 4})
    assert m.left == 3
    assert m.right == 4
    assert m.top == 12
    assert m.bottom == 0


def test_padding_dict_construction_incomplete() -> None:
    m = Padding({"top": 12})
    assert m.top == 12
    assert m.left == 0
    assert m.right == 0
    assert m.bottom == 0


def test_padding_negative_values() -> None:
    with raises(ValueError):
        Padding(-1)
    with raises(ValueError):
        Padding({"top": -1})
