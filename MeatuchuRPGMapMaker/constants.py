from enum import Enum
from typing import Literal


class DEPLOY_STAGE(Enum):
    PROD = "prod"
    BETA = "beta"
    DEV = "dev"
