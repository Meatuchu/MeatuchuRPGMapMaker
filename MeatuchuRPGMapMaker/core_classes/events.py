from typing import Any, Callable, Literal, Optional


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

    def __init__(self) -> None:
        super().__init__()


class CloseWindowEvent(UpdateEvent):
    # Fired when a window is closed
    name: str = "CloseWindowEvent"

    def __init__(self, window_name: Optional[str] = None) -> None:
        super().__init__(window_name=window_name)


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


class MouseMoveEvent(InputEvent):
    # Fired when the mouse is moved
    name: str = "MouseMoveEvent"

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x=x, y=y)


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

    def __init__(self) -> None:
        super().__init__()
