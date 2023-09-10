from enum import Enum
from typing import Literal
from .constants import DEPLOY_STAGE
from . import STAGE


class _MSG_LEVEL(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    INFO = "INFO"


class Logger:
    stage: DEPLOY_STAGE

    def __init__(self, stage: str = STAGE) -> None:
        self.stage = DEPLOY_STAGE(stage)

    def log(
        self,
        msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO"],
        msg: str,
    ) -> None:
        t = _MSG_LEVEL(msg_level)
        if self._should_log(t):
            print(msg)

    def _should_log(self, msg_level: _MSG_LEVEL) -> bool:
        if msg_level == _MSG_LEVEL.ERROR:
            return True
        if msg_level == _MSG_LEVEL.WARNING:
            return self.stage in [DEPLOY_STAGE.BETA, DEPLOY_STAGE.DEV]
        if msg_level == _MSG_LEVEL.INFO:
            return self.stage in [DEPLOY_STAGE.BETA, DEPLOY_STAGE.DEV]
        if msg_level == _MSG_LEVEL.DEBUG:
            return self.stage in [DEPLOY_STAGE.DEV]
        return False
