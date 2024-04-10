# pyright: reportImportCycles=false
import importlib
from typing import Any, Dict, Literal, Optional

from .RenderEvent import RenderEvent


class SceneChangeRequestEvent(RenderEvent):
    # Fire this event to request a scene be loaded on a particular window
    def __init__(
        self,
        scene_target: Literal[
            "MenuScene",
            "MapEditScene",
        ],
        window_name: Optional[str] = None,
        scene_kwargs: Dict[str, Any] = {},
    ) -> None:
        from MeatuchuRPGMapMaker.ui.scenes import Scene

        scene_module = importlib.import_module("MeatuchuRPGMapMaker.ui.scenes")
        scene_class = getattr(scene_module, scene_target)

        if not issubclass(scene_class, Scene):
            raise ValueError(f"{scene_target} is not a subclass of Scene")

        self.scene_to_load = scene_class
        self.window_name = window_name
        self.scene_kwargs = scene_kwargs
        super().__init__()
