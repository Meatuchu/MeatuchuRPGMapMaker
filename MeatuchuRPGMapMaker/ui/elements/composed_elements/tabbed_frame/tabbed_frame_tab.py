from MeatuchuRPGMapMaker.ui.elements.primitive_elements import Button, Element, Frame


class TabbedFrameTab:
    btn: Button
    frame: Frame
    frame_contents: list[Element]
    visible: bool = False

    def __init__(self, btn: Button, frame: Frame) -> None:
        self.btn = btn
        self.frame = frame
        self.frame_contents = []
        self.visible = False
