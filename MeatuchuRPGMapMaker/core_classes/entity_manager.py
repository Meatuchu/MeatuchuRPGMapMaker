from uuid import uuid4
from ..entities import BaseEntity
from typing import Dict


class EntityManager:
    storage: Dict[str, BaseEntity]

    def __init__(self) -> None:
        self.storage = {}
        pass

    def insert_entity(self, ent: BaseEntity) -> None:
        ent.set_id(self._get_id())
        self.storage[ent.id] = ent
        return

    def _get_id(self) -> str:
        return str(uuid4())

    def get_entity_by_id(self, id: str) -> BaseEntity:
        return self.storage[id]
