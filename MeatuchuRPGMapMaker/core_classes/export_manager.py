from . import FeatureManager
from .event_manager import EventManager


class ExportManager(FeatureManager):
    event_mgr: EventManager

    def __build__(self) -> None:
        pass

    def subscribe_to_events(self) -> None:
        pass
