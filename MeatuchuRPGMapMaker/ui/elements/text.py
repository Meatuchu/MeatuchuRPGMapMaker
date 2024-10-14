from element import Element


class Text(Element):
    ALLOW_CHILDREN: bool = False
    text: str

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def render(self):
        pass
