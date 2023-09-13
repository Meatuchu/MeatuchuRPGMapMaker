from typing import List, Optional, Tuple
from .wall_tile import WallTile
from .floor_tile import FloorTile


class RPGMapLayer:
    width = 40
    height = 40

    floor_tiles: List[List[Optional[FloorTile]]]
    wall_tiles: List[List[Optional[WallTile]]]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.floor_tiles = [[None] * width] * height
        self.wall_tiles = [[None] * width] * height

    def get_tiles_at_position(
        self,
        x: int,
        y: int,
    ) -> Tuple[Optional[FloorTile], Optional[WallTile]]:
        return self.floor_tiles[x][y], self.wall_tiles[x][y]


class RPGMapBoard:
    layers: List[RPGMapLayer]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.layers = []
        self.layers.append(RPGMapLayer(width, height))

    def get_tiles_at_position(
        self, x: int, y: int, z: int
    ) -> Tuple[Optional[FloorTile], Optional[WallTile]]:
        return self.layers[z].get_tiles_at_position(x, y)

    def get_all_tiles_at_position(
        self, x: int, y: int
    ) -> List[Tuple[Optional[FloorTile], Optional[WallTile]]]:
        r: List[Tuple[Optional[FloorTile], Optional[WallTile]]] = []
        for l in self.layers:
            r.append(l.get_tiles_at_position(x, y))
        return r
