from typing import List
from ..entities import WallTile, FloorTile


class Board:
    width = 40
    height = 40
    layers = 1

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height


class Layer:
    width = 40
    height = 40

    floor_tiles: List[List[FloorTile]] = [[]]
    wall_tiles: List[List[WallTile]] = [[]]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = 40
        self.height = 40
