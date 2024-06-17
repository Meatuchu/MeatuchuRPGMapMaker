from . import FeatureManager
from .event_manager import EventManager


class ExportManager(FeatureManager):
    event_mgr: EventManager

    def __init__(self) -> None:
        super().__init__()

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass
