import time

from MeatuchuRPGMapMaker.helpers import debounce

WAIT_VAL = 0.01


def test_debounce_before_time_limit() -> None:
    @debounce(WAIT_VAL)
    def f(x: int) -> int:
        return x

    assert f(0) == 0
    assert f(1) == 0


def test_debounce_after_time_limit() -> None:
    @debounce(WAIT_VAL)
    def f(x: int) -> int:
        return x

    assert f(0) == 0
    time.sleep(WAIT_VAL)
    assert f(2) == 2


def test_debounce_wrapped_prop() -> None:
    @debounce(WAIT_VAL)
    def f(x: int) -> int:
        return x

    assert f(0) == 0
    assert f(2) == 0
    assert f.__wrapped__(1) == 1
