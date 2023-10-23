from unittest.mock import MagicMock
import os

from MeatuchuRPGMapMaker.core_classes.texture_manager import TextureManager
from MeatuchuRPGMapMaker import ROOTDIR


def test_construction() -> None:
    assert TextureManager()


def test_load_all_textures() -> None:
    t = TextureManager()
    files = os.listdir(os.path.join(ROOTDIR, "../resources/textures"))
    for file in files:
        t.load_texture(file[0:-4])
    for file in files:
        assert t.get_texture(file[0:-4])


def test_register_event_manager() -> None:
    m = TextureManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_manager(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()
