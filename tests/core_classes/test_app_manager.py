from typing import Dict, NoReturn, cast
from unittest.mock import MagicMock

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
    managers = cast(Dict[str, MagicMock], a.get_all_managers())
    managers["event_mgr"].queue_scheduled_events = MagicMock(name="event_mgr.queue_scheduled_events")
    for k in managers:
        managers[k].input_step = MagicMock(name=f"{k}.input_step")
    a.input_step(0)
    for k in managers:
        managers[k].input_step.assert_called_once()
    managers["event_mgr"].queue_scheduled_events.assert_called_once()


def test_update_step() -> None:
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
    managers = cast(Dict[str, MagicMock], a.get_all_managers())
    managers["event_mgr"].queue_scheduled_events = MagicMock(name="event_mgr.queue_scheduled_events")
    for k in managers:
        managers[k].update_step = MagicMock(name=f"{k}.update_step")
    a.update_step(0)
    for k in managers:
        managers[k].update_step.assert_called_once()
    managers["event_mgr"].queue_scheduled_events.assert_called_once()


def test_render_step() -> None:
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
    managers = cast(Dict[str, MagicMock], a.get_all_managers())
    managers["event_mgr"].queue_scheduled_events = MagicMock(name="event_mgr.queue_scheduled_events")
    for k in managers:
        managers[k].render_step = MagicMock(name=f"{k}.render_step")
    a.render_step(0)
    for k in managers:
        managers[k].render_step.assert_called_once()
    managers["event_mgr"].queue_scheduled_events.assert_called_once()


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
