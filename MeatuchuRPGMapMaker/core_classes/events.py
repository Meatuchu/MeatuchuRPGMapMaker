from typing import Any, Callable, Dict, Literal, Optional, Tuple, Union


class Event:
    # Base Event Class
    # Subscribers to this class are invoked for all events
    name: str = "Event"
    args: Any
    kwargs: Any

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.args = args
        self.kwargs = kwargs


class InputEvent(Event):
    # Used only for processing user input
    name: str = "InputEvent"


class UpdateEvent(Event):
    # Used only for events relating to updating objects in memory
    name: str = "UpdateEvent"


class RenderEvent(Event):
    # Used only for events relating to rendering.
    name: str = "RenderEvent"


### INPUT EVENTS ###


class InputSnapshotEvent(InputEvent):
    # Emitted by InputManager on every input step - subscribe to this to get a collection of the current state of input
    name: str = "InputSnapshotEvent"

    def __init__(
        self,
        keys: Dict[str, int],
        mouse_buttons: Dict[str, Dict[str, Union[Tuple[int, int], int]]],
        mouse_position: Tuple[int, int],
    ) -> None:
        super().__init__(keys=keys, mouse_buttons=mouse_buttons, mouse_position=mouse_position)


class KeyPressEvent(InputEvent):
    # Fired when any key is pressed
    name: str = "KeyPressEvent"

    def __init__(self, key: str) -> None:
        super().__init__(key=key)


class KeyReleaseEvent(InputEvent):
    # Fired when any key is pressed
    name: str = "KeyReleaseEvent"

    def __init__(self, key: str, hold_time: float) -> None:
        super().__init__(key=key, hold_time=hold_time)


class MouseClickEvent(InputEvent):
    # Fired when a mouse button is pressed
    name: str = "MouseClickEvent"

    def __init__(self, button: str, position: Tuple[int, int]) -> None:
        super().__init__(button=button, position=position)


class MouseScrollEvent(InputEvent):
    name: str = "MouseScrollEvent"

    def __init__(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
    ) -> None:
        super().__init__(x=x, y=y, dx=dx, dy=dy)


class MouseClickReleaseEvent(InputEvent):
    # Fired when a mouse button is released
    name: str = "MouseClickReleaseEvent"

    def __init__(self, button: str, position: Tuple[int, int], hold_time: float) -> None:
        super().__init__(button=button, position=position, hold_time=hold_time)


class MouseMoveEvent(InputEvent):
    # Fired when the mouse is moved
    name: str = "MouseMoveEvent"

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x=x, y=y)


### UPDATE EVENTS ###


class NewThreadRequestEvent(UpdateEvent):
    # Fire this event to request a new thread from the ThreadManager
    name: str = "NewThreadRequestEvent"

    def __init__(
        self,
        thread_name: str,
        thread_target: Callable[..., None],
        owner_id: str,
    ) -> None:
        super().__init__(
            thread_name=thread_name,
            thread_target=thread_target,
            owner_id=owner_id,
        )


class NewThreadEvent(UpdateEvent):
    # Fired when a thread is created
    name: str = "NewThreadEvent"

    def __init__(
        self,
        thread_name: str,
    ) -> None:
        super().__init__(
            thread_name=thread_name,
        )


class DestroyThreadRequestEvent(UpdateEvent):
    # Fire this event to request ThreadManager to destroy a thread
    name: str = "DestroyThreadRequestEvent"

    def __init__(self, thread_name: str, owner_id: str) -> None:
        super().__init__(thread_name=thread_name, owner_id=owner_id)


class DestroyThreadEvent(UpdateEvent):
    # Fired when a thread is destroyed
    name: str = "DestroyThreadEvent"

    def __init__(self, thread_name: str) -> None:
        super().__init__(thread_name=thread_name)


class AllThreadsDestroyedEvent(UpdateEvent):
    # Fired when ThreadManager destroys its final thread.
    name: str = "AllThreadsDestroyedEvent"


class CloseWindowEvent(UpdateEvent):
    # Fired when a window is closed
    name: str = "CloseWindowEvent"

    def __init__(self, window_name: Optional[str] = None) -> None:
        super().__init__(window_name=window_name)


class WindowResizeRequestEvent(UpdateEvent):
    name: str = "WindowResizeRequestEvent"

    def __init__(self, width: int, height: int, window_name: Optional[str] = None) -> None:
        super().__init__(width=width, height=height, window_name=window_name)
        pass


class WindowFullscreenModeEditRequestEvent(UpdateEvent):
    name: str = "WindowFullscreenModeEditRequestEvent"

    def __init__(self, mode: Literal[0, 1, 2], window_name: Optional[str] = None) -> None:
        super().__init__(mode=mode, window_name=window_name)


class AppShutDownEvent(UpdateEvent):
    # Fired before app shuts down.
    # Subscribe to this event to be given a chance to perform cleanup
    name: str = "AppShutDownEvent"


class SceneChangeEvent(UpdateEvent):
    # Fired when the active scene is changed.
    name: str = "SceneChangeEvent"


### RENDER EVENTS ###
