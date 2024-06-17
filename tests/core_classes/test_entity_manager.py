from MeatuchuRPGMapMaker.core_classes.entity_manager import EntityManager
from MeatuchuRPGMapMaker.game.entities.base_entity import BaseEntity
from MeatuchuRPGMapMaker.game.entities.floor_entity import FloorEntity
from MeatuchuRPGMapMaker.game.entities.wall_entity import WallEntity


def test_insert_and_retrieve_entity() -> None:
    ents = [BaseEntity(), WallEntity(), FloorEntity()]
    mgr = EntityManager()
    for ent in ents:
        mgr.insert_entity(ent)
    for ent in ents:
        id = ent.id
        retrieved = mgr.get_entity_by_id(id)
        assert id
        assert retrieved == ent
