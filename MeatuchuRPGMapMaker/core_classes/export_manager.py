from . import FeatureManager
from .event_manager import EventManager


class ExportManager(FeatureManager):
    event_mgr: EventManager

    def __init__(self) -> None:
        super().__init__()

    def subscribe_to_events(self) -> None:
        pass
