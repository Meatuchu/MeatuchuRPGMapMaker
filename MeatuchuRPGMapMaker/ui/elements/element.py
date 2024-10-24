from tkinter import Tk as TkWindow
from uuid import uuid4

from ..types import Margin, Padding
from ..ui_consts import UIConstants


class Element:
    ALLOW_CHILDREN: bool = True

    margin: Margin
    padding: Padding
    width: int
    height: int
    children: list["Element"]
    id: str | None
    window: TkWindow
    parent: "Element | None"
    uuid: str

    def __init__(
        self,
        window: TkWindow,
        parent: "Element | None" = None,
        id: str | None = None,
    ) -> None:
        self.uuid = str(uuid4())
        self.window = window
        self.margin = Margin(UIConstants.Spacing.Fixed.xs)
        self.padding = Padding(UIConstants.Spacing.Fixed.xs)
        self.children = []
        self.id = id
        self.parent = parent

    def add_child(self, e: "Element") -> None:
        if self.ALLOW_CHILDREN:
            self.children.append(e)
        else:
            raise ValueError(f"{self.__class__.__name__} does not support child elements")

    def get_position_of_child_element(self, e: "Element") -> tuple[int, int]:
        return (0, 0)

    def get_absolute_position(self) -> tuple[int, int]:
        if self.parent:
            return self.parent.get_position_of_child_element(self)
        else:
            return (0, 0)

    def render(self) -> None:
        pass
