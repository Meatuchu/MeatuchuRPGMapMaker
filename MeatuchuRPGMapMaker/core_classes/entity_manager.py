from uuid import uuid4
from ..entities.base_entity import BaseEntity
from typing import Dict
from . import FeatureManager


class EntityManager(FeatureManager):
    storage: Dict[str, BaseEntity]

    def __init__(self) -> None:
        self.storage = {}
        super().__init__()
        pass

    def insert_entity(self, ent: BaseEntity) -> None:
        id = self._get_id()
        ent.set_id(id)
        self.storage[ent.id] = ent
        self.logger.log("DEBUG", f"Inserted {ent.id_name} into storage with id {id}")
        return

    def _get_id(self) -> str:
        id = str(uuid4())
        self.logger.log("DEBUG", f"Generated ID {id}")
        return id

    def get_entity_by_id(self, id: str) -> BaseEntity:
        return self.storage[id]
