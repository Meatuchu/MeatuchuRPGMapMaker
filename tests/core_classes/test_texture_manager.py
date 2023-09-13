from MeatuchuRPGMapMaker.core_classes.texture_manager import TextureManager


def test_construction() -> None:
    assert TextureManager()


def test_load():
    t = TextureManager()
    t.load_texture("cobblestone")
