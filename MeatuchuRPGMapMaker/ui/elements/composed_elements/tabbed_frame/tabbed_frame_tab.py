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

    def disable_button(self) -> None:
        self.btn.disable()
        self.btn.set_relief("sunken")

    def enable_button(self) -> None:
        self.btn.enable()
        self.btn.set_relief("raised")
