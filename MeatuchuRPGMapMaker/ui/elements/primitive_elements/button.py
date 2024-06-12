from tkinter import Button as TkButton
from tkinter import Tk as TkWindow
from typing import Callable, Literal

from MeatuchuRPGMapMaker.events import LogEvent

from .base_element import Element, ElementPlacingMode, ElementSizingMode


class Button(Element):
    _label: str
    x: int
    y: int
    x_offset: int
    y_offset: int
    width: int
    height: int
    _press_handler: Callable[..., None]
    _tkinter_button: TkButton

    def __init__(
        self,
        window: TkWindow,
        fire_event: Callable[..., None],
        name: str,
        label: str = "Button",
        x: int = 0,
        y: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        width: int = 300,
        height: int = 50,
        height_offset: int = 0,
        width_offset: int = 0,
        press_handler: Callable[..., None] = lambda: None,
        place_on_creation: bool = True,
        placing_mode: ElementPlacingMode = "absolute",
        sizing_mode: ElementSizingMode = "absolute",
    ) -> None:
        self._label = label
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.set_press_handler(press_handler)
        self._tkinter_button = TkButton(
            master=window,
            text=label,
            command=self.press_handler,
        )
        super().__init__(
            window,
            fire_event,
            name,
            place_on_creation=place_on_creation,
            placing_mode=placing_mode,
            sizing_mode=sizing_mode,
        )

    def place(self) -> None:
        width, height = self.get_adjusted_wh()
        if self.placing_mode == "absolute":
            self._tkinter_button.place(
                x=self.x + self.x_offset,
                y=self.y + self.y_offset,
                width=width,
                height=height,
            )
        elif self.placing_mode == "relative":
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            position_x = (self.x * window_width / 100) + self.x_offset
            position_y = (self.y * window_height / 100) + self.y_offset
            self._tkinter_button.place(
                x=position_x,
                y=position_y,
                width=width,
                height=height,
            )
        return super().place()

    def set_press_handler(self, handler: Callable[..., None]) -> None:
        self._press_handler = handler

    def press_handler(self) -> None:
        try:
            self._press_handler()
        except Exception as e:
            self._fire_event(
                LogEvent(
                    "ERROR", f"Uncaught {e.__class__.__name__} in {self.name} Press Handler! \n{str(e)}", self.name
                )
            )

    def hide(self) -> None:
        self._tkinter_button.place_forget()
        return super().hide()

    def destroy(self) -> None:
        self._tkinter_button.destroy()
        return super().destroy()

    def disable(self) -> None:
        self._tkinter_button.config(state="disabled")

    def enable(self) -> None:
        self._tkinter_button.config(state="normal")

    def set_relief(self, relief: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]) -> None:
        self._tkinter_button.config(relief=relief)
