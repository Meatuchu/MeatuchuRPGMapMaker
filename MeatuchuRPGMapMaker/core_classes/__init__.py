from typing import Any, Literal, Self
from uuid import uuid4

from MeatuchuRPGMapMaker.constants import DEPLOY_STAGE
from MeatuchuRPGMapMaker.logger import logger_factory


class FeatureManager:
    stage: DEPLOY_STAGE
    id: str
    event_mgr = None
    instance: Self | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.name = self.__class__.__name__
        self._logger = logger_factory()
        self.stage = self._logger.stage
        self.log("INFO", f"initializing {self.name}")

    def input_step(self, frame_number: int) -> None:
        pass

    def render_step(self, frame_number: int) -> None:
        pass

    def update_step(self, frame_number: int) -> None:
        pass

    def log(
        self,
        level: Literal["ERROR", "WARNING", "DEBUG", "INFO", "VERBOSE"],
        msg: str,
    ) -> None:
        self._logger.log(level, msg, self.name)
