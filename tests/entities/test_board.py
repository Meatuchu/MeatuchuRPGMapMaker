from MeatuchuRPGMapMaker.entities.board import RPGMapBoard, RPGMapLayer


def test_board_can_be_constructed() -> None:
    assert RPGMapBoard()
    assert RPGMapBoard(2, 2)


def test_layer_can_be_constructed() -> None:
    assert RPGMapLayer()
    assert RPGMapLayer(2, 2)
