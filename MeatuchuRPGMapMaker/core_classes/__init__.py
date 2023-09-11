from ..logger import logger_factory


class FeatureManager:
    stage: str

    def __init__(self) -> None:
        self.logger = logger_factory()
        self.stage = self.logger.stage.value
        self.logger.log("DEBUG", f"initializing {self.__class__.__name__}")
        pass
