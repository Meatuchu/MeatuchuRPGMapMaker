# Ignore unused imports in this file, since they are used to expose the classes to the rest of the codebase
# pyright: reportUnusedImport=false

from typing import Any

from .AllThreadsDestroyedEventClass import AllThreadsDestroyedEvent
from .AppShutDownEventClass import AppShutDownEvent
from .CloseWindowEventClass import CloseWindowEvent
from .DestroyThreadEventClass import DestroyThreadEvent
from .DestroyThreadRequestEventClass import DestroyThreadRequestEvent
from .EditSettingRequestEventClass import EditSettingRequestEvent
from .EventClass import Event
from .FileSaveRequestEventClass import FileSaveRequestEvent
from .InputEventClass import InputEvent
from .InputSnapshotEventClass import InputSnapshotEvent
from .KeyPressEventClass import KeyPressEvent
from .KeyReleaseEventClass import KeyReleaseEvent
from .LogEventClass import LogEvent
from .MouseClickEventClass import MouseClickEvent
from .MouseClickReleaseEventClass import MouseClickReleaseEvent
from .MouseMoveEventClass import MouseMoveEvent
from .MouseScrollEventClass import MouseScrollEvent
from .NewThreadEventClass import NewThreadEvent
from .NewThreadRequestEventClass import NewThreadRequestEvent
from .RenderEventClass import RenderEvent
from .SceneChangeEventClass import SceneChangeEvent
from .SceneChangeRequestEventClass import SceneChangeRequestEvent
from .SettingEditedEventClass import SettingEditedEvent
from .ThreadErrorEventClass import ThreadErrorEvent
from .UpdateEventClass import UpdateEvent
from .WindowFullscreenModeEditRequestEventClass import (
    WindowFullscreenModeEditRequestEvent,
)
from .WindowResizedEventClass import WindowResizedEvent
from .WindowResizeRequestEventClass import WindowResizeRequestEvent
from .WindowToggleFullscreenModeRequestEventClass import (
    WindowToggleFullscreenModeRequestEvent,
)

type EventQueueItemType = Event | dict[str, Any]
type EventQueueType = list[EventQueueItemType]

EventSubscriptionArgType = type[Event] | str
