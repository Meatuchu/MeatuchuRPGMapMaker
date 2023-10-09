from typing import NoReturn
from unittest.mock import MagicMock, call

from pytest import raises
from MeatuchuRPGMapMaker.core_classes.app_manager import AppManager


def test_app_manager_creation() -> None:
    AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )


def test_app_manager_does_update_on_should_tick() -> None:
    # setup
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    a.should_do_game_tick = lambda cur_time: True
    a.input_step = MagicMock()
    a.update_step = MagicMock()

    # test
    a.app_frame_process()

    # assertions
    a.input_step.assert_called()
    a.update_step.assert_called()


def test_app_manager_does_update_on_should_tick_neg() -> None:
    # setup
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    a.should_do_game_tick = lambda cur_time: False
    a.input_step = MagicMock()
    a.update_step = MagicMock()

    # test
    a.app_frame_process()

    # assertions
    a.input_step.assert_not_called()
    a.update_step.assert_not_called()


def test_activate_app() -> None:
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    original = a.app_frame_process
    a.state.tickgap = 0

    class EndLoopForTest(Exception):
        pass

    def mock_app_frame_process() -> NoReturn:
        original()
        raise EndLoopForTest()

    a.app_frame_process = mock_app_frame_process

    with raises(EndLoopForTest):
        a.activate_app()


def test_should_do_game_tick_negative() -> None:
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )

    a.state.last_update_time = 0
    a.state.tickgap = 12
    assert not a.should_do_game_tick(1)


def test_should_do_game_tick_positive() -> None:
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )

    a.state.last_update_time = 0
    a.state.tickgap = 12
    assert a.should_do_game_tick(12)


def test_input_step() -> None:
    features = MagicMock()
    features.input_step = MagicMock()
    a = AppManager(features, features, features, features, features, features, features, features, features)
    a.input_step(0)
    features.input_step.assert_has_calls(
        [
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
        ]
    )


def test_update_step() -> None:
    features = MagicMock()
    features.update_step = MagicMock()
    a = AppManager(
        features,
        features,
        features,
        features,
        features,
        features,
        features,
        features,
        features,
    )
    a.update_step(0)
    features.update_step.assert_has_calls(
        [
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
            call(0),
        ]
    )


def test_init_board() -> None:
    a = AppManager(
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    a.open_new_map()
