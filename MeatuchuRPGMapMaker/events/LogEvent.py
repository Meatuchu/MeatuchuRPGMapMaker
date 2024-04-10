from typing import Literal

from .Event import Event


class LogEvent(Event):
    msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO"]
    msg: str

    def __init__(self, msg_level: Literal["ERROR", "WARNING", "DEBUG", "INFO"], msg: str) -> None:
        super().__init__()
        self.msg_level = msg_level
        self.msg = msg