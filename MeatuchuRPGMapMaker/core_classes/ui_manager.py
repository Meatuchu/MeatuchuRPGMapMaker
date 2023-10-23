from . import FeatureManager
from .event_manager import EventManager
from ..ui.scenes.scene import Scene
from .events import SceneChangeEvent


class UIManager(FeatureManager):
    event_mgr: EventManager
    _active_scene: Scene

    def __init__(self) -> None:
        super().__init__()

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass

    def activate_scene(self, new_scene: Scene) -> None:
        self._active_scene = new_scene
        self.event_mgr.queue_event(SceneChangeEvent())
