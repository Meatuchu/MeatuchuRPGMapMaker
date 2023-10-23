import tkinter as tk
from typing import Literal, Dict, Callable, Optional, cast
from datetime import datetime

from . import FeatureManager
from .event_manager import EventManager
from .events import (
    CloseWindowEvent,
    NewThreadRequestEvent,
    DestroyThreadRequestEvent,
    WindowResizeRequestEvent,
    WindowFullscreenModeEditRequestEvent,
)

DEFAULT_WINDOW_NAME = "main"


class WindowManager(FeatureManager):
    event_mgr: EventManager
    _windows: Dict[str, Optional[tk.Tk]]
    _canvases: Dict[str, tk.Canvas]

    def __init__(self) -> None:
        self._windows = {}
        self._canvases = {}
        super().__init__()

    def _get_window_thread(self, window_name: str = DEFAULT_WINDOW_NAME) -> Callable[[], None]:
        def _ret() -> None:
            window_obj = tk.Tk()
            window_obj.title(window_name if window_name != DEFAULT_WINDOW_NAME else "Meatuchu's RPG Map Maker")
            canvas_obj = tk.Canvas(window_obj)
            canvas_obj.pack()
            self._windows[window_name] = window_obj
            self._canvases[window_name] = canvas_obj
            self.log("INFO", f"Activating window {window_name}")

            window_obj.mainloop()
            del self._windows[window_name]
            del self._canvases[window_name]
            self.event_mgr.queue_event(CloseWindowEvent(window_name))
            self.event_mgr.queue_event(DestroyThreadRequestEvent(f"{window_name}_window_thread", self.id))

        return _ret

    def create_window(self, window_name: str = DEFAULT_WINDOW_NAME) -> None:
        self._windows[window_name] = None  # Marks the window as being queued for creation
        if not self.event_mgr:
            raise ValueError("Cannot create window before we have an event manager!")

        if self._canvases.get(window_name) or self._windows.get(window_name):
            raise ValueError(f"Window {window_name} already exists!")

        self.event_mgr.queue_event(
            NewThreadRequestEvent(f"{window_name}_window_thread", self._get_window_thread(window_name), self.id)
        )

        self.log("DEBUG", f"Requested thread for {window_name} window")

    def set_window_size(self, event: WindowResizeRequestEvent) -> None:
        width = event.kwargs.get("width", 800)
        height = event.kwargs.get("height", 600)
        window_name = event.kwargs.get("window_name", DEFAULT_WINDOW_NAME) or DEFAULT_WINDOW_NAME
        t = datetime.now().timestamp()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > 1:
                    raise RuntimeError(
                        "Took too long to wait for window creation while resizing! Is there something wrong with the window create thread?"
                    )
            cast(tk.Tk, self._windows[window_name]).geometry(f"{width}x{height}")
            self._canvases[window_name].config(width=width, height=height)
            self._canvases[window_name].pack()
            self.log(
                "DEBUG",
                f"set side window {window_name} size to {width} by {height}",
            )
        except KeyError:
            raise KeyError(f"Cannot set window size, {window_name} window does not exist")

    def set_fullscreen_mode(self, event: WindowFullscreenModeEditRequestEvent) -> None:
        mode = event.kwargs.get("mode")
        window_name = event.kwargs.get("window_name", DEFAULT_WINDOW_NAME) or DEFAULT_WINDOW_NAME
        t = datetime.now().timestamp()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > 1:
                    raise RuntimeError(
                        "Took too long to wait for window creation while resizing! Is there something wrong with the window create thread?"
                    )
            cast(tk.Tk, self._windows[window_name]).attributes("-fullscreen", mode >= 1)
            self.log(
                "DEBUG",
                f"set {window_name} fullscreen mode to {mode}",
            )
        except KeyError:
            raise KeyError(f"Cannot set fullscreen mode for {window_name} window, it doesn't exist!")

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        self.event_mgr.register_subscription(WindowResizeRequestEvent, self.set_window_size)
        self.event_mgr.register_subscription(WindowFullscreenModeEditRequestEvent, self.set_fullscreen_mode)
        pass
