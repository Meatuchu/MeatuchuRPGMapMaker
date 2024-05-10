# Disable pyright reportImportCycles because imports are at runtime
# pyright: reportImportCycles=false
import importlib
import inspect
from types import ModuleType
from typing import Any, Dict, Optional

from .RenderEvent import RenderEvent


class SceneChangeRequestEvent(RenderEvent):
    # Fire this event to request a scene be loaded on a particular window
    def __init__(
        self,
        scene_target: str,
        window_name: Optional[str] = None,
        scene_kwargs: Dict[str, Any] = {},
    ) -> None:
        from MeatuchuRPGMapMaker.ui.scenes import Scene

        # Need to import at construction time due to circular import.
        scene_module = importlib.import_module("MeatuchuRPGMapMaker.ui.scenes")

        try:
            scene_class = getattr(scene_module, scene_target)
        except AttributeError:
            raise AttributeError(
                f'Unable to find scene "{scene_target}"!{get_available_scenes_from_module(scene_module)}'
            )

        if not inspect.isclass(scene_class) or not issubclass(scene_class, Scene):
            raise ValueError(
                f'Attempted to fire SceneChangeRequestEvent for invalid scene "{scene_target}"!{get_available_scenes_from_module(scene_module)}'
            )

        self.scene_to_load = scene_class
        self.window_name = window_name
        self.scene_kwargs = scene_kwargs
        super().__init__()


def get_available_scenes_from_module(mod: ModuleType) -> str:
    from MeatuchuRPGMapMaker.ui.scenes import Scene

    scenes = "\n    ".join(
        [
            scene_name
            for scene_name in dir(mod)
            if inspect.isclass(getattr(mod, scene_name)) and issubclass(getattr(mod, scene_name), Scene)
        ]
    )

    return f"\n\nAvailable Scenes:\n    {scenes}\n"
