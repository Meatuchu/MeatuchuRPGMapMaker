import tkinter as tk
from typing import Literal


class WindowManager:
    def __init__(self) -> None:
        self.window = tk.Tk()

    def activate_window(self) -> None:
        self.window.mainloop()

    def set_window_size(self, width: int = 800, height: int = 600) -> None:
        self.window.geometry(f"{width}x{height}")

    def set_fullscreen_mode(self, mode: Literal[0, 1, 2]):
        self.window.attributes("-fullscreen", True)
        pass
