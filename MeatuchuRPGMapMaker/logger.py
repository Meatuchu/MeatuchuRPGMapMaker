import traceback
from datetime import datetime
from enum import Enum
from typing import Callable, Literal, Optional

from colorama import Fore, Style

from . import STAGE_STR, VERBOSE_FLAG
from .constants import DEPLOY_STAGE


def get_cur_time() -> datetime:
    return datetime.now()


class _MSG_LEVEL(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    INFO = "INFO"
    VERBOSE = "VERBOSE"


MsgLevelType = Literal["ERROR", "WARNING", "DEBUG", "INFO", "VERBOSE"]


class Logger:
    stage: DEPLOY_STAGE
    verbose: bool
    should_print_color: bool
    _colors = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "INFO": Fore.WHITE,
        "DEBUG": Fore.CYAN,
        "VERBOSE": Fore.MAGENTA,
    }

    def __init__(self, stage: Optional[Literal["prod", "beta", "dev"]] = None) -> None:
        self.stage = DEPLOY_STAGE(stage or STAGE_STR)
        self.verbose = VERBOSE_FLAG
        self.should_print_color = True

    def toggle_colored_print(self) -> None:
        self.should_print_color = not self.should_print_color

    def log(
        self,
        msg_level: MsgLevelType,
        msg: str,
        module: str = "",
    ) -> None:
        t = _MSG_LEVEL(msg_level)
        # Used to align messages by their label
        level_label_gap = " " * (max((7 - len(msg_level)), 0) + 1)
        if self._should_log(t):
            tlabel = f"[{get_cur_time().strftime('%Y-%m-%d %H:%M:%S.%f')}] {msg_level}"
            tlabel = f"{tlabel}{level_label_gap}{module}" if module else tlabel
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
        if msg_level == _MSG_LEVEL.VERBOSE:
            return self.verbose

    def _color_msg(self, msg_level: _MSG_LEVEL, msg: str) -> str:
        if self.should_print_color:
            return self._colors[msg_level.value] + msg + Style.RESET_ALL
        return msg

    def handle_exception(self, e: Exception) -> None:
        if self.stage is DEPLOY_STAGE.PROD:
            self.log("ERROR", "Critical error has occurred...")
        else:
            err_name = (
                e.__class__.__name__
                if not self.should_print_color
                else self._colors["ERROR"] + e.__class__.__name__ + Style.RESET_ALL
            )
            self.log(
                "ERROR",
                f"An unhandled {err_name} has occurred with message: {str(e)}",
            )
            self.log("ERROR", traceback.format_exc())


def _logger_retriever() -> Callable[[], Logger]:
    inst = Logger()
    return lambda: inst


logger_factory = _logger_retriever()
