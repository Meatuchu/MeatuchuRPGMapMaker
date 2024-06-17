from uuid import uuid4

from MeatuchuRPGMapMaker.game.entities.base_entity import BaseEntity

from . import FeatureManager
from .event_manager import EventManager


class EntityManager(FeatureManager):
    storage: dict[str, BaseEntity]
    event_mgr: EventManager

    def __init__(self) -> None:
        self.storage = {}
        super().__init__()

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass

    def insert_entity(self, ent: BaseEntity) -> None:
        id = self._get_id()
        ent.set_id(id)
        self.storage[ent.id] = ent
        self.log("INFO", f"Inserted {ent.id_name} into storage with id {id}")
        return

    def _get_id(self) -> str:
        id = str(uuid4())
        self.log("VERBOSE", f"Generated ID {id}")
        return id

    def get_entity_by_id(self, id: str) -> BaseEntity:
        return self.storage[id]
