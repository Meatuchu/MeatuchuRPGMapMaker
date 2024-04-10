# pyright: reportImportCycles=false
from typing import Any, Dict, Optional, Type

from ..ui.scenes.scene import Scene
from .RenderEvent import RenderEvent


class SceneChangeRequestEvent(RenderEvent):
    # Fire this event to request a scene be loaded on a particular window
    def __init__(
        self, scene_to_load: Type[Scene], window_name: Optional[str] = None, scene_kwargs: Dict[str, Any] = {}
    ) -> None:
        self.window_name = window_name
        self.scene_to_load = scene_to_load
        self.scene_kwargs = scene_kwargs
        super().__init__()
