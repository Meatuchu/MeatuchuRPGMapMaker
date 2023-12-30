from tkinter import Tk as TkWindow

from ....exceptions import ElementNotNamedError, ElementCreatedWithoutWindowError


class Element:
    name: str

    def __init__(
        self,
        window: TkWindow,
        name: str,
    ) -> None:
        if not name:
            raise (ElementNotNamedError(self.__class__.__name__))
        if not window:
            raise (ElementCreatedWithoutWindowError(self.__class__.__name__))
        self.name = name

    def destroy(self) -> None:
        pass
