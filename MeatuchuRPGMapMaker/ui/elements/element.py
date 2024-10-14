from typing import Self

from ..ui_consts import UIConstants


class Element:
    ALLOW_CHILDREN: bool = True

    margin: int
    padding: int
    children: list[Self]
    id: str | None

    def __init__(self, id=None) -> None:
        self.margin = UIConstants.Spacing.Fixed.xs
        self.padding = UIConstants.Spacing.Fixed.xs
        self.children = []
        self.id = id
        pass

    def render(self):
        pass
