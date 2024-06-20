from typing import Literal

from .EventClass import Event


class LogEvent(Event):
    msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO", "VERBOSE"]
    msg: str
    src: str

    def __init__(
        self, msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO", "VERBOSE"], msg: str, src: str = "LogEvent"
    ) -> None:
        super().__init__()
        self.msg_level = msg_level
        self.msg = msg
        self.src = src
