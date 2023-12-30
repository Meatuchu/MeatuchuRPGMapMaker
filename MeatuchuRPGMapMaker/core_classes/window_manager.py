from tkinter import Tk as TkWindow, Canvas as TkCanvas
from typing import Dict, Callable, Optional
from datetime import datetime

from . import FeatureManager
from .event_manager import EventManager
from .events import (
    CloseWindowEvent,
    NewThreadRequestEvent,
    DestroyThreadRequestEvent,
    WindowResizeRequestEvent,
    WindowFullscreenModeEditRequestEvent,
    SceneChangeRequestEvent,
)
from ..ui.scenes.scene import Scene
from ..exceptions import DuplicateWindowError, WindowNotExistError, WindowNotFoundError

DEFAULT_WINDOW_NAME = "main"


class FPSMeasure:
    def __init__(
        self,
        window_name: str,
        logfn: Callable[..., None],
        afterfn: Callable[..., Optional[str]],
    ) -> None:
        self.frames = 0
        self.logfn = logfn
        self.afterfn = afterfn
        self.window_name = window_name
        self.afterfn(100, self.inc_frames)
        self.afterfn(1000, self.get_fps)

    def inc_frames(self) -> None:
        self.frames += 1
        self.afterfn(0, self.inc_frames)

    def get_fps(self) -> None:
        self.logfn("DEBUG", f"Window {self.window_name} FPS: {self.frames}")
        self.frames = 0
        self.afterfn(1000, self.get_fps)


class WindowManager(FeatureManager):
    event_mgr: EventManager
    _windows: Dict[str, Optional[TkWindow]]
    _canvases: Dict[str, TkCanvas]
    _scenes: Dict[str, Scene]

    def __init__(self) -> None:
        self._windows = {}
        self._canvases = {}
        self._scenes = {}
        super().__init__()

    def _get_window_thread(
        self,
        window_name: str = DEFAULT_WINDOW_NAME,
    ) -> Callable[[], None]:
        def _ret() -> None:
            window_obj = TkWindow()
            window_obj.title(window_name if window_name != DEFAULT_WINDOW_NAME else "Meatuchu's RPG Map Maker")
            canvas_obj = TkCanvas(window_obj)
            canvas_obj.pack()
            self._windows[window_name] = window_obj
            self._canvases[window_name] = canvas_obj
            self.log("INFO", f"Activating window {window_name}")

            FPSMeasure(window_name, self.log, window_obj.after)

            window_obj.mainloop()

            self.log("DEBUG", f"window {window_name} was closed")
            if self._scenes.get(window_name):
                del self._scenes[window_name]
            del self._windows[window_name]
            del self._canvases[window_name]
            self.event_mgr.queue_event(CloseWindowEvent(window_name))
            self.event_mgr.queue_event(DestroyThreadRequestEvent(f"{window_name}_window_thread", self.id))

        return _ret

    def create_window(self, window_name: str = DEFAULT_WINDOW_NAME) -> None:
        self._windows[window_name] = None  # Marks the window as being queued for creation

        if self._canvases.get(window_name) or self._windows.get(window_name):
            raise DuplicateWindowError(window_name)

        self.event_mgr.queue_event(
            NewThreadRequestEvent(f"{window_name}_window_thread", self._get_window_thread(window_name), self.id)
        )

        self.log("DEBUG", f"Requested thread for {window_name} window")

    def set_window_size(self, event: WindowResizeRequestEvent) -> None:
        width = event.width or 800
        height = event.height or 600
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        t = datetime.now().timestamp()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > 1:
                    raise WindowNotFoundError(window_name)
            window = self._windows[window_name]
            assert window
            window.geometry(f"{width}x{height}")
            self._canvases[window_name].config(width=width, height=height)
            self._canvases[window_name].pack()
            self.log(
                "DEBUG",
                f"set side window {window_name} size to {width} by {height}",
            )
        except KeyError:
            raise WindowNotExistError(window_name)

    def set_fullscreen_mode(self, event: WindowFullscreenModeEditRequestEvent) -> None:
        mode = event.mode
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        t = datetime.now().timestamp()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > 1:
                    raise WindowNotFoundError(window_name)
            window = self._windows[window_name]
            assert window
            window.attributes("-fullscreen", mode >= 1)  # type: ignore
            self.log(
                "DEBUG",
                f"set {window_name} fullscreen mode to {mode}",
            )
        except KeyError:
            raise WindowNotExistError(window_name)

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        self.event_mgr.register_subscription(WindowResizeRequestEvent, self.set_window_size)
        self.event_mgr.register_subscription(WindowFullscreenModeEditRequestEvent, self.set_fullscreen_mode)
        self.event_mgr.register_subscription(SceneChangeRequestEvent, self.load_scene)
        pass

    def load_scene(self, event: SceneChangeRequestEvent) -> None:
        t = datetime.now().timestamp()
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        scene = event.scene_to_load
        old_scene = self._scenes.get(window_name)
        if old_scene:
            old_scene.unload()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > 1:
                    raise WindowNotFoundError(window_name)
            window = self._windows[window_name]
            assert window
            self._scenes[window_name] = scene(window)
            self.log(
                "DEBUG",
                f"loaded scene {self._scenes[window_name].name} to window {window_name}",
            )
        except KeyError:
            raise WindowNotExistError(window_name)
