import time
from datetime import datetime
from tkinter import Canvas as TkCanvas
from tkinter import Tk as TkWindow
from typing import Callable

from MeatuchuRPGMapMaker.events import (
    CloseWindowEvent,
    DestroyThreadRequestEvent,
    Event,
    NewThreadRequestEvent,
    RenderEvent,
    SceneChangeEvent,
    SceneChangeRequestEvent,
    SettingEditedEvent,
    WindowFullscreenModeEditRequestEvent,
    WindowResizedEvent,
    WindowResizeRequestEvent,
    WindowToggleFullscreenModeRequestEvent,
)
from MeatuchuRPGMapMaker.exceptions import (
    DuplicateWindowError,
    WindowNotExistError,
    WindowNotFoundError,
)
from MeatuchuRPGMapMaker.helpers import debounce
from MeatuchuRPGMapMaker.ui.scene.scene import Scene

from . import FeatureManager
from .event_manager import EventManager

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
            self.logfn("VERBOSE", f"Window {self.window_name} FPS: {self.frames}")
            self.frames = 0


class WindowManager(FeatureManager):
    event_mgr: EventManager
    _windows: dict[str, TkWindow | None]
    _canvases: dict[str, TkCanvas]
    _scenes: dict[str, Scene]
    _window_events: dict[str, list[RenderEvent]]
    _outgoing_events: list[Event]

    window_create_timeout = 0.1

    def __init__(self) -> None:
        self._windows = {}
        self._canvases = {}
        self._scenes = {}
        self._window_events = {}
        self._outgoing_events = []
        super().__init__()

    def _get_window_thread(
        self,
        window_name: str = DEFAULT_WINDOW_NAME,
    ) -> Callable[[], None]:
        def _ret() -> None:
            class WindowStatus:
                active = True
                fullscreen_mode: int = 0
                size_width: int = 0
                size_height: int = 0

                @classmethod
                def set_inactive(cls) -> None:
                    WindowStatus.active = False

                @classmethod
                def set_fullscreen(cls, mode: int) -> None:
                    WindowStatus.fullscreen_mode = mode

                @classmethod
                @debounce(0.25)
                def set_size(cls, width: int, height: int, scene: Scene) -> None:
                    if width <= 0 or height <= 0:
                        raise ValueError("Width and height must be greater than 0")
                    if WindowStatus.size_width != width or WindowStatus.size_height != height:
                        WindowStatus.size_width = width
                        WindowStatus.size_height = height
                        self.event_mgr.queue_event(WindowResizedEvent(width, height, window_name))
                        scene.handle_window_resize()

            def handle_event(event: Event) -> None:
                if isinstance(event, WindowResizeRequestEvent):
                    self.set_window_size(event)
                elif isinstance(event, WindowFullscreenModeEditRequestEvent):
                    WindowStatus.set_fullscreen(event.mode)
                    self.set_fullscreen_mode(event)
                elif isinstance(event, WindowToggleFullscreenModeRequestEvent):
                    mode = 1 if WindowStatus.fullscreen_mode == 0 else 0
                    WindowStatus.set_fullscreen(mode)
                    self.set_fullscreen_mode(WindowFullscreenModeEditRequestEvent(mode, event.window_name))
                elif isinstance(event, SceneChangeRequestEvent):
                    self.load_scene(event)

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
            window_obj.protocol("WM_DELETE_WINDOW", WindowStatus.set_inactive)

            # Start the mainloop
            fps = FPSMeasure(window_name, self.log)
            try:
                while WindowStatus.active:
                    if self._scenes.get(window_name):
                        self._scenes[window_name].tick_update()
                        self._scenes[window_name].frame_update()
                        try:
                            WindowStatus.set_size(
                                window_obj.winfo_width(), window_obj.winfo_height(), self._scenes[window_name]
                            )
                        except Exception as e:
                            self.log("WARNING", f"window {window_name} encountered an error: {e}")
                    window_obj.update()
                    window_obj.update_idletasks()
                    fps.inc_frames()
                    fps.get_fps()
                    while len(self._window_events[window_name]):
                        handle_event(self._window_events[window_name].pop(0))

            except Exception as err:
                self.log("ERROR", f"window {window_name} encountered an error: {err.__class__.__name__}: {str(err)}")

            # Window is closed, clean up
            window_obj.destroy()
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
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        self._wait_for_window(window_name)
        window = self._windows[window_name]
        assert window
        width = event.width or window.winfo_width()
        height = event.height or window.winfo_height()
        window.geometry(f"{width}x{height}")
        self._canvases[window_name].config(width=width, height=height)
        self._canvases[window_name].pack()
        self.log(
            "DEBUG",
            f"set side window {window_name} size to {width} by {height}",
        )

    def set_fullscreen_mode(self, event: WindowFullscreenModeEditRequestEvent) -> None:
        mode = event.mode
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        self._wait_for_window(window_name)
        window = self._windows[window_name]
        assert window
        window.attributes("-fullscreen", mode >= 1)  # pyright: ignore[reportUnknownMemberType]
        self.log(
            "DEBUG",
            f"set {window_name} fullscreen mode to {mode}",
        )

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        self.event_mgr.register_subscription(WindowResizeRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(WindowToggleFullscreenModeRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(WindowFullscreenModeEditRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(SceneChangeRequestEvent, self.pass_event_to_window_queue)
        self.event_mgr.register_subscription(SettingEditedEvent, self.handle_settings_change)
        pass

    def pass_event_to_window_queue(self, event: RenderEvent) -> None:
        window_name = event.window_name or DEFAULT_WINDOW_NAME
        self._window_events[window_name] = self._window_events.get(window_name, [])
        self._window_events[window_name].append(event)

    def load_scene(self, event: SceneChangeRequestEvent) -> None:
        self.log("DEBUG", f"loading scene {event.scene_to_load.__name__}")

        window_name = event.window_name or DEFAULT_WINDOW_NAME
        scene = event.scene_to_load

        self._wait_for_window(window_name)
        window = self._windows[window_name]
        assert window

        try:
            # Grab old scene
            old_scene = self._scenes.get(window_name)

            # Create new scene
            self._scenes[window_name] = scene(
                window,
                window_name,
                self._outgoing_events.append,
                self.event_mgr.register_subscription,
                self.event_mgr.unregister_subscription,
                **event.scene_kwargs,
            )

            # Unload old scene
            if old_scene:
                old_scene.unload()

            self.log(
                "VERBOSE",
                f"loaded scene {self._scenes[window_name].name} to window {window_name}",
            )

            # Queue event to notify the scene has changed
            self.event_mgr.queue_event(SceneChangeEvent())

        except Exception as e:
            self.log("ERROR", f"failed to load scene {scene.__name__} to window {window_name}: {e}")
            raise e

    def _wait_for_window(self, window_name: str) -> None:
        try:
            time = datetime.now().timestamp()
            while not self._windows[window_name]:  # Wait until window is created, if the key exists but is none.
                if datetime.now().timestamp() - time > self.window_create_timeout:
                    raise WindowNotFoundError(window_name)
        except KeyError:
            raise WindowNotExistError(window_name)

    def handle_settings_change(self, event: SettingEditedEvent) -> None:
        if event.group == "window":
            if event.key == "width":
                self.pass_event_to_window_queue(WindowResizeRequestEvent(event.value, None))
            elif event.key == "height":
                self.pass_event_to_window_queue(WindowResizeRequestEvent(None, event.value))
            elif event.key == "fullscreen_mode":
                self.pass_event_to_window_queue(WindowFullscreenModeEditRequestEvent(event.value))

    def input_step(self, frame_number: int) -> None:
        return super().input_step(frame_number)

    def update_step(self, frame_number: int) -> None:
        return super().update_step(frame_number)

    def render_step(self, frame_number: int) -> None:
        while self._outgoing_events:
            self.event_mgr.queue_event(self._outgoing_events.pop(0))
        return super().render_step(frame_number)
