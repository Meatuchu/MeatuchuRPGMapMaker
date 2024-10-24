from typing import Literal


class Margin:
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, input: int | dict[Literal["top", "bottom", "left", "right"], int]) -> None:
        self.set_value(input)

    def set_value(self, input: int | dict[Literal["top", "bottom", "left", "right"], int]) -> None:
        if type(input) is int:
            if input < 0:
                raise ValueError("Margins must be positive!")
            self.left = input
            self.right = input
            self.top = input
            self.bottom = input
        elif type(input) is dict:
            for value in input.values():
                if value < 0:
                    raise ValueError("Margins must be positive!")
            self.left = input.get("left", 0)
            self.right = input.get("right", 0)
            self.top = input.get("top", 0)
            self.bottom = input.get("bottom", 0)


class Padding:
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, input: int | dict[Literal["top", "bottom", "left", "right"], int]) -> None:
        self.set_value(input)

    def set_value(self, input: int | dict[Literal["top", "bottom", "left", "right"], int]) -> None:
        if type(input) is int:
            if input < 0:
                raise ValueError("Margins must be positive!")
            self.left = input
            self.right = input
            self.top = input
            self.bottom = input
        elif type(input) is dict:
            for value in input.values():
                if value < 0:
                    raise ValueError("Margins must be positive!")
            self.left = input.get("left", 0)
            self.right = input.get("right", 0)
            self.top = input.get("top", 0)
            self.bottom = input.get("bottom", 0)
