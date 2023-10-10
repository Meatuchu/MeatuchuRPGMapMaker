from typing import Literal
from uuid import uuid4
from ..logger import logger_factory
from ..constants import DEPLOY_STAGE


class FeatureManager:
    stage: DEPLOY_STAGE
    id: str
    event_mgr = None

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.name = self.__class__.__name__
        self._logger = logger_factory()
        self.stage = self._logger.stage
        self.log("INFO", f"initializing {self.name}")
        pass

    def input_step(self, frame_number: int) -> None:
        pass

    def render_step(self, frame_number: int) -> None:
        pass

    def update_step(self, frame_number: int) -> None:
        pass

    def log(
        self,
        level: Literal["ERROR", "WARNING", "DEBUG", "INFO"],
        msg: str,
    ) -> None:
        self._logger.log(level, msg, self.name)
