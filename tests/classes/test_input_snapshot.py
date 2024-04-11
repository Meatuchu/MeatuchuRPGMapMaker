from MeatuchuRPGMapMaker.classes.input_snapshot import InputSnapshot


def test_construction() -> None:
    assert InputSnapshot
    assert InputSnapshot({"a": 0}, {}, (0, 0))
