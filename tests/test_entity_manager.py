from MeatuchuRPGMapMaker.core_classes.entity_manager import EntityManager
from MeatuchuRPGMapMaker.entities import BaseEntity


def test_insert_and_retrieve_entity() -> None:
    ent = BaseEntity()
    mgr = EntityManager()
    mgr.insert_entity(ent)
    id = ent.id
    retrieved = mgr.get_entity_by_id(id)
    assert id
    assert retrieved == ent
