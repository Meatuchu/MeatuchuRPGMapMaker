from .element import Element


class Div(Element):
    ALLOW_CHILDREN: bool = True

    def __init__(self) -> None:
        super().__init__()

    def render(self):
        pass
