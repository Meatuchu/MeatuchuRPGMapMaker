import tkinter as tk
from typing import Literal, Dict, Optional
from . import FeatureManager
from PIL import ImageTk


class WindowManager(FeatureManager):
    name = "WindowManager"

    def __init__(self) -> None:
        self._side_windows: Dict[str, tk.Tk] = {}
        self._side_canvases: Dict[str, tk.Canvas] = {}

        self._main_window = tk.Tk()
        self._main_canvas = tk.Canvas(self._main_window)
        self._main_canvas.pack()
        super().__init__()

    def activate_window(self, window: Optional[str] = None) -> None:
        if not window:
            self._main_window.mainloop()
            self.logger.log(
                "DEBUG",
                "activated main window",
                self.name,
            )
        else:
            self._side_windows[window].mainloop()
            self.logger.log(
                "DEBUG",
                f"activated side window {window}",
                self.name,
            )

    def create_window(self, name: str) -> None:
        if not self._side_windows.get(name):
            self._side_windows[name] = tk.Tk()
            self._side_canvases[name] = tk.Canvas(self._side_windows[name])
            self._side_canvases[name].pack()
            self.logger.log("DEBUG", f"created window {name}", self.name)
        else:
            raise KeyError(f"Window {name} already exists!")

    def set_window_size(
        self,
        width: int = 800,
        height: int = 600,
        window: Optional[str] = None,
    ) -> None:
        if not window:
            self._main_window.geometry(f"{width}x{height}")
            self._main_canvas.config(width=width, height=height)
            self._main_canvas.pack()
            self.logger.log(
                "DEBUG",
                f"set main window size to {width} by {height}",
                self.name,
            )
        else:
            self._side_windows[window].geometry(f"{width}x{height}")
            self._side_canvases[window].config(width=width, height=height)
            self._side_canvases[window].pack()
            self.logger.log(
                "DEBUG",
                f"set side window {window} size to {width} by {height}",
                self.name,
            )

    def set_fullscreen_mode(
        self,
        mode: Literal[0, 1, 2],
        window: Optional[str] = None,
    ) -> None:
        target_window = self._main_window if not window else self._side_windows[window]
        tw_str = "main window" if not window else f"side window {window}"
        if mode >= 1:
            target_window.attributes("-fullscreen", True)
        elif mode == 0:
            target_window.attributes("-fullscreen", False)
        self.logger.log(
            "DEBUG",
            f"set {tw_str} fullscreen mode to {mode}",
            self.name,
        )
