from ..constants import LOGGER_LEVEL, STAGE


class Logger:
    log_levels = ["ERROR", "WARN", "INFO", "DEBUG"]

    def __init__(self, stage: str) -> None:
        self.stage = stage
        pass

    def log(self, msg_level: LOGGER_LEVEL.TYPE, msg: str) -> None:
        if self._should_log(msg_level):
            print(msg)

    def _should_log(self, msg_level: LOGGER_LEVEL.TYPE) -> bool:
        if msg_level == LOGGER_LEVEL.ERROR:
            return True
        if msg_level == LOGGER_LEVEL.WARNING:
            return self.stage in [STAGE.BETA, STAGE.DEV]
        if msg_level == LOGGER_LEVEL.INFO:
            return self.stage in [STAGE.BETA, STAGE.DEV]
        if msg_level == LOGGER_LEVEL.DEBUG:
            return self.stage in [STAGE.DEV]
        return False
