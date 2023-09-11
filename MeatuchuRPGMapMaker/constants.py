from enum import Enum


class DEPLOY_STAGE(Enum):
    PROD = "prod"
    BETA = "beta"
    DEV = "dev"
