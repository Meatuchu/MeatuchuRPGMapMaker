import os

from MeatuchuRPGMapMaker import ROOTDIR
from MeatuchuRPGMapMaker.core_classes.texture_manager import TextureManager


def test_construction() -> None:
    assert TextureManager()


def test_load_all_textures() -> None:
    t = TextureManager()
    files = os.listdir(os.path.join(ROOTDIR, "../resources/textures"))
    for file in files:
        t.load_texture(file[0:-4])
    for file in files:
        assert t.get_texture(file[0:-4])
