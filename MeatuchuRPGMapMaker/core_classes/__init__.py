from abc import abstractmethod, ABC
from typing import Any, Literal, Self, final
from uuid import uuid4

from MeatuchuRPGMapMaker.constants import DEPLOY_STAGE
from MeatuchuRPGMapMaker.logger import logger_factory


class FeatureManager(ABC):
    stage: DEPLOY_STAGE
    id: str
    event_mgr = None
    _instance: Self | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @final
    def __init__(self) -> None:
        if self._initialized:
            return

        self.id = str(uuid4())
        self.name = self.__class__.__name__
        self._logger = logger_factory()
        self.stage = self._logger.stage
        self.log("INFO", f"initializing {self.name}")
        self.__build__()

        self._initialized = True

    @abstractmethod
    def __build__(self) -> None:
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
        self._logger.log(level, msg, self.name)
