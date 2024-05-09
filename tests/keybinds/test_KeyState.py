# pyright: reportPrivateUsage=false
import time

from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot
from MeatuchuRPGMapMaker.keybinds.KeyState import KeyState


def test_construct_keystate() -> None:
    assert KeyState({"ctrl": 0, "alt": 0, "delete": 0})


def test_check_simple_keystate_pos() -> None:
    ks = KeyState({"a": 0})
    assert ks.check(InputSnapshot({"a": time.time_ns() - 100}, {}, (0, 0)))


def test_check_simple_keystate_neg() -> None:
    ks = KeyState({"a": 0})
    assert not ks.check(InputSnapshot({"b": 100}, {}, (0, 0)))


def test_check_modifier_keystate_pos() -> None:
    ks = KeyState({"ctrl": 0, "a": 0})
    assert ks.check(
        InputSnapshot(
            keys={
                "a": 1000,
                "ctrl": 600,
            },
            mouse_buttons={},
            mouse_position=(0, 0),
        )
    )


def test_check_modifier_keystate_neg_not_all_pressed() -> None:
    ks = KeyState({"ctrl": 0, "a": 0})
    assert not ks.check(
        InputSnapshot(
            keys={
                "ctrl": 600,
            },
            mouse_buttons={},
            mouse_position=(0, 0),
        )
    )


def test_check_modifier_keystate_neg_modifier_pressed_last() -> None:
    ks = KeyState({"ctrl": 0, "a": 0})
    assert not ks.check(
        InputSnapshot(
            keys={
                "a": 0,
                "ctrl": 600,
            },
            mouse_buttons={},
            mouse_position=(0, 0),
        )
    )


def test_check_modifier_keystate_pos_modifier_pressed_last() -> None:
    ks = KeyState({"ctrl": 0, "a": 0}, modifiers_first=False)
    assert ks.check(
        InputSnapshot(
            keys={
                "a": 100,
                "ctrl": 600,
            },
            mouse_buttons={},
            mouse_position=(0, 0),
        )
    )


def test_check_keystate_refire() -> None:
    ks = KeyState({"a": 0})
    assert not ks.get_is_fired()
    assert ks.check(InputSnapshot({"a": time.time_ns() - 100}, {}, (0, 0)))
    assert ks.get_is_fired()
    assert not ks.check(InputSnapshot({"a": time.time_ns() - 100}, {}, (0, 0)))
    assert ks.get_is_fired()


def test_check_keystate_refire_allowed() -> None:
    ks = KeyState({"a": 0}, allow_hold_refire=True)
    assert not ks.get_is_fired()
    assert ks.check(InputSnapshot({"a": time.time_ns() - 100}, {}, (0, 0)))
    assert ks.get_is_fired()
    assert ks.check(InputSnapshot({"a": time.time_ns() - 100}, {}, (0, 0)))
    assert ks.get_is_fired()


def test_check_keystate_fired_not_global() -> None:
    ks1 = KeyState({"a": 0})
    ks2 = KeyState({"a": 0})
    ks1.check(InputSnapshot({"a": 1}, {}, (0, 0)))
    assert ks1.get_is_fired()
    assert not ks2.get_is_fired()
