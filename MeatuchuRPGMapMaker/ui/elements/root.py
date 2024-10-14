from .element import Element


class Root(Element):
    ALLOW_CHILDREN: bool = True
    ids: set[str]

    def __init__(self, scene_path: str) -> None:
        super().__init__(id="root")
        self.margin = 0
        self.padding = 0

    def render(self):
        pass

    def parse(self):
        pass
