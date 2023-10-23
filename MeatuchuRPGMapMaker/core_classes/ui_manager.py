from typing import Dict

from . import FeatureManager
from .event_manager import EventManager
from ..ui_elements.base_element import Element


class UIManager(FeatureManager):
    event_mgr: EventManager
    ui_elements: Dict[str, Element]

    def __init__(self) -> None:
        super().__init__()

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass
