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
        ent.set_id(self._get_id())
        self.storage[ent.id] = ent
        return

    def _get_id(self) -> str:
        return str(uuid4())

    def get_entity_by_id(self, id: str) -> BaseEntity:
        return self.storage[id]
