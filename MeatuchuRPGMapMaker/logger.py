from enum import Enum
from typing import Callable, Literal
from datetime import datetime
from colorama import Fore, Style

from .constants import DEPLOY_STAGE
from . import STAGE


class _MSG_LEVEL(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    INFO = "INFO"


class Logger:
    stage: DEPLOY_STAGE
    should_print_color: bool
    _colors = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "INFO": Fore.WHITE,
        "DEBUG": Fore.CYAN,
    }

    def __init__(self, stage: str = STAGE) -> None:
        self.stage = DEPLOY_STAGE(stage)
        self.should_print_color = True

    def toggle_colored_print(self) -> None:
        self.should_print_color = not self.should_print_color

    def log(
        self,
        msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO"],
        msg: str,
        module: str = "",
    ) -> None:
        t = _MSG_LEVEL(msg_level)
        # Used to align messages by their label
        level_label_gap = " " * max((7 - len(msg_level)), 0)
        if self._should_log(t):
            tlabel = f"[{datetime.now().strftime('%Y-%m-%-d %H:%M:%S.%f')}] {msg_level}{level_label_gap}"
            tlabel = f"{tlabel} {module}" if module else tlabel
            clabel = self._color_msg(t, tlabel)
            print(f"{clabel}: {msg}")

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

    def _color_msg(self, msg_level: _MSG_LEVEL, msg: str) -> str:
        if self.should_print_color:
            return self._colors[msg_level.value] + msg + Style.RESET_ALL
        return msg


def _logger_retriever() -> Callable[[], Logger]:
    inst = Logger()
    return lambda: inst


logger_factory = _logger_retriever()
