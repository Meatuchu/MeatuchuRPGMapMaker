from typing import Any
from unittest.mock import MagicMock


class VeryMagicMock(MagicMock):
    """
    VeryMagicMock is a subclass of MagicMock. Any undefined attribute of the mock is initialized as a VeryMagicMock when it is accessed, so you won't need to define nested mocks.
    """

    def __getattribute__(self, __name: str) -> MagicMock:
        try:
            return super().__getattribute__(__name)
        except:
            super().__setattr__(__name, VeryMagicMock())
            return super().__getattribute__(__name)

    def __init__(self) -> None:
        pass
