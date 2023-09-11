from MeatuchuRPGMapMaker.core_classes.entity_manager import EntityManager
from MeatuchuRPGMapMaker.entities.base_entity import BaseEntity
from MeatuchuRPGMapMaker.entities.wall_tile import WallTile
from MeatuchuRPGMapMaker.entities.floor_tile import FloorTile


def test_insert_and_retrieve_entity() -> None:
    ents = [BaseEntity(), WallTile(), FloorTile()]
    mgr = EntityManager()
    for ent in ents:
        mgr.insert_entity(ent)
    for ent in ents:
        id = ent.id
        retrieved = mgr.get_entity_by_id(id)
        assert id
        assert retrieved == ent
