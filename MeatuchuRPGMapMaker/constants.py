from typing import Literal


class STAGE:
    PROD = "prod"
    BETA = "beta"
    DEV = "dev"
    TYPE = Literal["prod", "beta", "dev"]


class LOGGER_LEVEL:
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    INFO = "INFO"
    TYPE = Literal["ERROR", "WARNING", "DEBUG", "INFO"]
