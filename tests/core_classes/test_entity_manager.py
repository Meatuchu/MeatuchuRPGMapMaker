from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes.entity_manager import EntityManager
from MeatuchuRPGMapMaker.entities.base_entity import BaseEntity
from MeatuchuRPGMapMaker.entities.wall_entity import WallEntity
from MeatuchuRPGMapMaker.entities.floor_entity import FloorEntity


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


def test_register_event_manager() -> None:
    m = EntityManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_mgr(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
