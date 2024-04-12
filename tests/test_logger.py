# pyright: reportPrivateUsage=false
from datetime import datetime
from unittest.mock import MagicMock, call, patch

from pytest import raises

from MeatuchuRPGMapMaker.constants import DEPLOY_STAGE
from MeatuchuRPGMapMaker.logger import _MSG_LEVEL, Logger, logger_factory


def test_logger_prod_logs() -> None:
    logger = Logger("prod")
    assert logger._should_log(_MSG_LEVEL("ERROR"))
    assert not logger._should_log(_MSG_LEVEL("WARNING"))
    assert not logger._should_log(_MSG_LEVEL("INFO"))
    assert not logger._should_log(_MSG_LEVEL("DEBUG"))


def test_logger_beta_logs() -> None:
    logger = Logger("beta")
    assert logger._should_log(_MSG_LEVEL("ERROR"))
    assert logger._should_log(_MSG_LEVEL("WARNING"))
    assert logger._should_log(_MSG_LEVEL("INFO"))
    assert not logger._should_log(_MSG_LEVEL("DEBUG"))


def test_logger_dev_logs() -> None:
    logger = Logger("dev")
    assert logger._should_log(_MSG_LEVEL("ERROR"))
    assert logger._should_log(_MSG_LEVEL("WARNING"))
    assert logger._should_log(_MSG_LEVEL("INFO"))
    assert logger._should_log(_MSG_LEVEL("DEBUG"))


def test_logger_log() -> None:
    for stage in DEPLOY_STAGE:
        logger = Logger(stage.value)
        for level in _MSG_LEVEL:
            logger.log(level.value, "test_msg")


def test_logger_log_verbose() -> None:
    for stage in DEPLOY_STAGE:
        logger = Logger(stage.value)
        logger.verbose = True
        for level in _MSG_LEVEL:
            logger.log(level.value, "test_msg")


def test_logger_invalid_stage() -> None:
    with raises(ValueError):
        Logger("invalid value")  # pyright: ignore[reportArgumentType]


def test_logger_log_negative() -> None:
    logger = Logger("prod")
    with raises(ValueError):
        logger.log("invalid value", "test")  # pyright: ignore[reportArgumentType]


def test_logger_factory_returns_same_instance() -> None:
    l1 = logger_factory()
    l2 = logger_factory()

    assert l1 == l2


def test_logger_toggle_should_print_color() -> None:
    a = Logger("prod")
    init = a.should_print_color
    a.toggle_colored_print()
    assert a.should_print_color is not init


def test_logger_handle_error_preprod() -> None:
    a = Logger("dev")
    a.log = MagicMock()
    a.toggle_colored_print()
    try:
        raise Exception("test")
    except Exception as e:
        a.handle_exception(e)
    a.log.assert_has_calls(calls=[call("ERROR", "An unhandled Exception has occurred with message: test")])


def test_logger_handle_error_prod() -> None:
    a = Logger("prod")
    a.log = MagicMock()
    a.toggle_colored_print()
    try:
        raise Exception("test")
    except Exception as e:
        a.handle_exception(e)
    a.log.assert_has_calls(calls=[call("ERROR", "Critical error has occurred...")])


@patch(
    "MeatuchuRPGMapMaker.logger.get_cur_time",
    MagicMock(return_value=datetime(2077, 1, 1, 1, 1, 1, 1)),
)
@patch("MeatuchuRPGMapMaker.logger.print")
def test_logger_logs(mock_print: MagicMock) -> None:
    a = Logger("prod")
    a.should_print_color = False
    a.log("ERROR", "test")
    mock_print.assert_has_calls([call("[2077-01-01 01:01:01.000001] ERROR: test")])
