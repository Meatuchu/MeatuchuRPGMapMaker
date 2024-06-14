import os
import traceback
from datetime import datetime
from enum import Enum
from io import TextIOWrapper
from shutil import copyfile
from typing import Callable, Literal

from colorama import Fore, Style

from . import STAGE_STR, VERBOSE_FLAG, get_arg_value
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
    should_write_to_file: bool
    silent: bool
    file: TextIOWrapper | None
    __log_file_name: str
    _colors = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "INFO": Fore.WHITE,
        "DEBUG": Fore.CYAN,
        "VERBOSE": Fore.MAGENTA,
    }

    def __init__(
        self,
        stage: Literal["prod", "beta", "dev"] | None = None,
    ) -> None:
        self.stage = DEPLOY_STAGE(stage or STAGE_STR)
        self.verbose = VERBOSE_FLAG
        self.silent = get_arg_value("--silent") or False
        self.should_print_color = True
        self.file = None
        self.should_write_to_file = False

    def open_log_file(self) -> None:
        if not self.should_write_to_file:
            self.__log_file_name = f"logs/{get_cur_time().strftime('%Y_%m_%d-%H_%M_%S')}_log.txt"
            self.file = open(self.__log_file_name, "w")
            self.should_write_to_file = True

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
        tlabel = f"[{get_cur_time().strftime('%Y-%m-%d %H:%M:%S.%f')}] {msg_level}"
        tlabel = f"{tlabel}{level_label_gap}{module}" if module else tlabel
        if self.should_write_to_file and self.file:
            self.file.write(f"{tlabel}: {msg}\n")
        if self._should_log(t):
            clabel = self._color_msg(t, tlabel)
            self.print(f"{clabel}: {msg}")

    def print(self, msg: str) -> None:
        if not self.silent:
            print(msg)

    def _should_log(self, msg_level: _MSG_LEVEL) -> bool:
        if self.verbose:
            return True
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

    def close_file(self) -> None:
        if self.should_write_to_file and self.file:
            if os.path.exists("logs/latest.txt"):
                os.remove("logs/latest.txt")
            self.should_write_to_file = False
            self.file.close()
            copyfile(self.__log_file_name, "logs/latest.txt")
            self.file = None


def _logger_retriever() -> Callable[[], Logger]:
    inst = Logger()
    return lambda: inst


logger_factory = _logger_retriever()
