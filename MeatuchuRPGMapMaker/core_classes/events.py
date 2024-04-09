from datetime import datetime
from typing import Any, Callable, Dict, Literal, Optional, Tuple, Type, Union

from ..ui.scenes.scene import Scene


class Event:
    # Base Event Class
    # Subscribers to this class are invoked for all events
    def __init__(self) -> None:
        self.created_at = datetime.now().timestamp()


class InputEvent(Event):
    # Used only for processing user input
    pass


class UpdateEvent(Event):
    # Used only for events relating to updating objects in memory
    pass


class RenderEvent(Event):
    # Used only for events relating to rendering and windows
    window_name: Optional[str]
    pass


### INPUT EVENTS ###


class InputSnapshotEvent(InputEvent):
    # Emitted by InputManager on every input step - subscribe to this to get a collection of the current state of input
    def __init__(
        self,
        keys: Dict[str, int],
        mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]],
        mouse_position: Tuple[int, int],
    ) -> None:
        self.keys = keys
        self.mouse_buttons = mouse_buttons
        self.mouse_postion = mouse_position
        super().__init__()


class KeyPressEvent(InputEvent):
    # Fired when any key is pressed
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__()


class KeyReleaseEvent(InputEvent):
    # Fired when any key is pressed
    def __init__(self, key: str, hold_time: float) -> None:
        self.key = key
        self.hold_time = hold_time
        super().__init__()


class MouseClickEvent(InputEvent):
    # Fired when a mouse button is pressed
    def __init__(self, button: str, position: Tuple[int, int]) -> None:
        self.button = button
        self.position = position
        super().__init__()


class MouseScrollEvent(InputEvent):
    # Fired when the mousewheel is scrolled
    def __init__(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
    ) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        super().__init__()


class MouseClickReleaseEvent(InputEvent):
    # Fired when a mouse button is released
    def __init__(self, button: str, position: Tuple[int, int], hold_time: float) -> None:
        self.button = button
        self.position = position
        self.hold_time = hold_time
        super().__init__()


class MouseMoveEvent(InputEvent):
    # Fired when the mouse is moved
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__()


### UPDATE EVENTS ###


class NewThreadRequestEvent(UpdateEvent):
    # Fire this event to request a new thread from the ThreadManager
    def __init__(
        self,
        thread_name: str,
        thread_target: Callable[..., None],
        owner_id: str,
    ) -> None:
        self.thread_name = thread_name
        self.thread_target = thread_target
        self.owner_id = owner_id
        super().__init__()


class NewThreadEvent(UpdateEvent):
    # Fired when a thread is created
    def __init__(
        self,
        thread_name: str,
    ) -> None:
        self.thread_name = thread_name
        super().__init__()


class DestroyThreadRequestEvent(UpdateEvent):
    # Fire this event to request ThreadManager to destroy a thread
    def __init__(self, thread_name: str, owner_id: str) -> None:
        self.thread_name = thread_name
        self.owner_id = owner_id
        super().__init__()


class DestroyThreadEvent(UpdateEvent):
    # Fired when a thread is destroyed
    def __init__(self, thread_name: str) -> None:
        self.thread_name = thread_name
        super().__init__()


class AllThreadsDestroyedEvent(UpdateEvent):
    # Fired when ThreadManager destroys its final thread.
    pass


class CloseWindowEvent(UpdateEvent):
    # Fired when a window is closed
    def __init__(self, window_name: Optional[str] = None) -> None:
        self.window_name = window_name
        super().__init__()


class AppShutDownEvent(UpdateEvent):
    # Fired before the app shuts down. This is the final event to be processed.
    # Subscribe to this event to be given a chance to perform cleanup
    pass


class SceneChangeEvent:
    # Fired when the active scene is changed.
    pass


### RENDER EVENTS ###
class WindowResizeRequestEvent(RenderEvent):
    # Fired when a window has been resized
    def __init__(self, width: int, height: int, window_name: Optional[str] = None) -> None:
        self.width = width
        self.height = height
        self.window_name = window_name
        super().__init__()


class WindowFullscreenModeEditRequestEvent(RenderEvent):
    # Fire this event to request a window's fullscreen mode be updated
    def __init__(self, mode: Literal[0, 1, 2], window_name: Optional[str] = None) -> None:
        self.mode = mode
        self.window_name = window_name
        super().__init__()


class SceneChangeRequestEvent(RenderEvent):
    # Fire this event to request a scene be loaded on a particular window
    def __init__(
        self, scene_to_load: Type[Scene], window_name: Optional[str] = None, scene_kwargs: Dict[str, Any] = {}
    ) -> None:
        self.window_name = window_name
        self.scene_to_load = scene_to_load
        self.scene_kwargs = scene_kwargs
        super().__init__()


### EXCEPTION EVENTS ###
class ThreadErrorEvent(Event):
    # Base class for thread errors
    def __init__(self, thread_name: str, owner_id: str, exception: Exception) -> None:
        self.thread_name = thread_name
        self.owner_id = owner_id
        self.exception = exception
        super().__init__()
