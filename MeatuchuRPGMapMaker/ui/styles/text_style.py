class TextStyle:
    FONT: str
    SIZE: int
    pass


class Normal(TextStyle):
    FONT = "arial"
    SIZE = 16


class H1(Normal):
    FONT = "consolas"
    SIZE = 48


class H2(H1):
    SIZE = 36
