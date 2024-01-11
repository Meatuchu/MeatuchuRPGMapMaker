import time
from tkinter import Tk as TkWindow, Canvas as TkCanvas

from typing import Dict, Callable, List, Optional, cast
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
    Event,
)
from ..ui.scenes.scene import Scene
from ..exceptions import DuplicateWindowError, WindowNotExistError, WindowNotFoundError

DEFAULT_WINDOW_NAME = "main"


class FPSMeasure:
    def __init__(
        self,
        window_name: str,
        logfn: Callable[..., None],
    ) -> None:
        self.frames = 0
        self.logfn = logfn
        self.window_name = window_name
        self.last_print = time.time()

    def inc_frames(self) -> None:
        self.frames += 1

    def get_fps(self) -> None:
        if time.time() - self.last_print > 1:
            self.last_print = time.time()
            self.logfn("DEBUG", f"Window {self.window_name} FPS: {self.frames}")
            self.frames = 0


class WindowManager(FeatureManager):
    event_mgr: EventManager
    _windows: Dict[str, Optional[TkWindow]]
    _canvases: Dict[str, TkCanvas]
    _scenes: Dict[str, Scene]
    _window_events: Dict[str, List[Event]]

    window_create_timeout = 5.0

    def __init__(self) -> None:
        self._windows = {}
        self._canvases = {}
        self._scenes = {}
        self._window_events = {}
        super().__init__()

    def _get_window_thread(
        self,
        window_name: str = DEFAULT_WINDOW_NAME,
    ) -> Callable[[], None]:
        def _ret() -> None:
            # window_active is used to determine if the window is still open
            window_active = True

            def set_window_inactive() -> None:
                self.log("ERROR", f"window {window_name} was closed")
                nonlocal window_active
                window_active = False

            # Create the window and canvas
            window_obj = TkWindow()
            window_obj.title(window_name if window_name != DEFAULT_WINDOW_NAME else "Meatuchu's RPG Map Maker")
            canvas_obj = TkCanvas(window_obj)
            canvas_obj.pack()
            self._windows[window_name] = window_obj
            self._canvases[window_name] = canvas_obj
            self._window_events[window_name] = self._window_events.get(window_name, [])
            self.log("INFO", f"Activating window {window_name}")

            # Set the window to close when the close button is pressed
            window_obj.protocol("WM_DELETE_WINDOW", set_window_inactive)

            # Start the mainloop
            fps = FPSMeasure(window_name, self.log)
            try:
                while window_active:
                    window_obj.update()
                    window_obj.update_idletasks()
                    fps.inc_frames()
                    fps.get_fps()
                    while len(self._window_events[window_name]):
                        event = self._window_events[window_name].pop(0)
                        if isinstance(event, WindowResizeRequestEvent):
                            self.set_window_size(event)
                        elif isinstance(event, WindowFullscreenModeEditRequestEvent):
                            self.set_fullscreen_mode(event)
                        elif isinstance(event, SceneChangeRequestEvent):
                            self.load_scene(event)
            except Exception as e:
                self.log("ERROR", f"window {window_name} encountered an error: {e}")

            # Window is closed, clean up
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
                if datetime.now().timestamp() - t > self.window_create_timeout:
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
            while not self._windows.get(window_name):  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > self.window_create_timeout:
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
        self.event_mgr.register_subscription(WindowResizeRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(WindowFullscreenModeEditRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(SceneChangeRequestEvent, self.pass_event_to_window_queue)
        pass

    _window_events: Dict[str, List[Event]] = {}

    def pass_event_to_window_queue(self, event: Event) -> None:
        window_name = cast(str, event.window_name or DEFAULT_WINDOW_NAME)  # type: ignore
        if self._windows[window_name] or True:
            self._window_events[window_name] = self._window_events.get(window_name, [])
            self._window_events[window_name].append(event)  # type: ignore

    def load_scene(self, event: SceneChangeRequestEvent) -> None:
        t = datetime.now().timestamp()
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        scene = event.scene_to_load
        old_scene = self._scenes.get(window_name)
        if old_scene:
            old_scene.unload()
        try:
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - t > self.window_create_timeout:
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
        except Exception as e:
            self.log("ERROR", f"failed to load scene {scene.name} to window {window_name}: {e}")
