from typing import List, Optional, Tuple
from .wall_entity import WallEntity
from .floor_entity import FloorEntity


class RPGMapLayer:
    width = 40
    height = 40

    floor_tiles: List[List[Optional[FloorEntity]]]
    wall_tiles: List[List[Optional[WallEntity]]]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.floor_tiles = [[None] * width] * height
        self.wall_tiles = [[None] * width] * height

    def get_tiles_at_position(
        self,
        x: int,
        y: int,
    ) -> Tuple[Optional[FloorEntity], Optional[WallEntity]]:
        return self.floor_tiles[x][y], self.wall_tiles[x][y]

    def get_tile_at_position_floor(self, x: int, y: int) -> Optional[FloorEntity]:
        try:
            return self.floor_tiles[x][y]
        except:
            return None

    def get_tile_at_position_wall(self, x: int, y: int) -> Optional[WallEntity]:
        try:
            return self.wall_tiles[x][y]
        except:
            return None

    def place_floor_at_position(self, x: int, y: int, tile: FloorEntity) -> None:
        self.floor_tiles[x][y] = tile

    def place_wall_at_position(self, x: int, y: int, tile: WallEntity) -> None:
        self.wall_tiles[x][y] = tile


class RPGMapBoard:
    layers: List[RPGMapLayer]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.layers = []
        self.layers.append(RPGMapLayer(width, height))

    def get_tiles_at_position(
        self, x: int, y: int, z: int
    ) -> Tuple[Optional[FloorEntity], Optional[WallEntity]]:
        return self.layers[z].get_tiles_at_position(x, y)

    def get_all_tiles_at_position(
        self, x: int, y: int
    ) -> List[Tuple[Optional[FloorEntity], Optional[WallEntity]]]:
        r: List[Tuple[Optional[FloorEntity], Optional[WallEntity]]] = []
        for l in self.layers:
            r.append(l.get_tiles_at_position(x, y))
        return r

    def place_floor_at_position_in_layer(
        self, x: int, y: int, z: int, tile: FloorEntity
    ) -> None:
        self.layers[z].place_floor_at_position(x, y, tile)

    def place_wall_at_position_in_layer(
        self, x: int, y: int, z: int, tile: WallEntity
    ) -> None:
        self.layers[z].place_wall_at_position(x, y, tile)

    def get_cell_neighbors_floor(
        self, x: int, y: int, z: int
    ) -> List[Optional[FloorEntity]]:
        return [
            self.layers[z].get_tile_at_position_floor(x - 1, y - 1),
            self.layers[z].get_tile_at_position_floor(x, y - 1),
            self.layers[z].get_tile_at_position_floor(x + 1, y - 1),
            self.layers[z].get_tile_at_position_floor(x - 1, y),
            self.layers[z].get_tile_at_position_floor(x + 1, y),
            self.layers[z].get_tile_at_position_floor(x - 1, y + 1),
            self.layers[z].get_tile_at_position_floor(x, y + 1),
            self.layers[z].get_tile_at_position_floor(x + 1, y + 1),
        ]

    def get_cell_neighbors_wall(
        self, x: int, y: int, z: int
    ) -> List[Optional[WallEntity]]:
        return [
            self.layers[z].get_tile_at_position_wall(x - 1, y - 1),
            self.layers[z].get_tile_at_position_wall(x, y - 1),
            self.layers[z].get_tile_at_position_wall(x + 1, y - 1),
            self.layers[z].get_tile_at_position_wall(x - 1, y),
            self.layers[z].get_tile_at_position_wall(x + 1, y),
            self.layers[z].get_tile_at_position_wall(x - 1, y + 1),
            self.layers[z].get_tile_at_position_wall(x, y + 1),
            self.layers[z].get_tile_at_position_wall(x + 1, y + 1),
        ]
