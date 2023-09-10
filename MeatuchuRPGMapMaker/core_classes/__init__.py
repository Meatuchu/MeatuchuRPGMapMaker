from ..logger import Logger
from MeatuchuRPGMapMaker import STAGE


class FeatureManager:
    stage: str

    def __init__(self) -> None:
        self.logger = Logger(STAGE)
        self.stage = STAGE
        self.logger.log("DEBUG", f"initializing {self.__class__.__name__}")
        pass
