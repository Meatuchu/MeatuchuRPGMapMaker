# pyright: reportPrivateUsage=false
from pytest import raises
from MeatuchuRPGMapMaker.core_classes.logger import Logger, _MSG_LEVEL
from MeatuchuRPGMapMaker.constants import DEPLOY_STAGE


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


def test_logger_invalid_stage() -> None:
    with raises(ValueError):
        Logger("invalid value")


def test_logger_log_negatice() -> None:
    logger = Logger("prod")
    with raises(ValueError):
        logger.log("invalid value", "test")  # type: ignore
