import importlib
from typing import Any, Literal, Self
from uuid import uuid4

from MeatuchuRPGMapMaker.constants import DEPLOY_STAGE
from MeatuchuRPGMapMaker.logger import logger_factory


class FeatureManager:
    id: str
    stage: DEPLOY_STAGE
    name: str
    _logger = logger_factory()
    instance: Self | None = None
    event_mgr = None
    init_finished = False

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.__init_logger()
        self.log("INFO", f"initializing {self.__class__.__name__}")

        if self.__class__.__name__ != "EventManager":
            event_mgr_mod = importlib.import_module("MeatuchuRPGMapMaker.core_classes.event_manager")
            self.event_mgr = event_mgr_mod.EventManager()

        self.subscribe_to_events()
        self.init_finished = True

    def __init_logger(self) -> None:
        self._logger = logger_factory()
        self.name = self.__class__.__name__
        self.stage = self._logger.stage

    def subscribe_to_events(self) -> None:
        pass

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
        if not self.init_finished:
            self.__init_logger()
        self._logger.log(level, msg, self.name)
