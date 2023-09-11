from typing import List
from . import WallTile, FloorTile


class RPGMapLayer:
    width = 40
    height = 40

    floor_tiles: List[List[FloorTile]] = [[]]
    wall_tiles: List[List[WallTile]] = [[]]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = 40
        self.height = 40


class RPGMapBoard:
    layers: List[RPGMapLayer] = []

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
