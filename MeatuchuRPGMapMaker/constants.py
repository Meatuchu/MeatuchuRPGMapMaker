from enum import Enum


class DEPLOY_STAGE(Enum):
    PROD = "prod"
    BETA = "beta"
    DEV = "dev"


NS_PER_MS = 1000000
NS_PER_S = 1000000000
