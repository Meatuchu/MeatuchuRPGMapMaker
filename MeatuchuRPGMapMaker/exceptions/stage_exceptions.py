from .base_exception import RPGMapException


class InvalidStageException(RPGMapException):
    def __init__(self, stage_recieved: str) -> None:
        super().__init__(f"An invalid stage was provided! {stage_recieved}")
