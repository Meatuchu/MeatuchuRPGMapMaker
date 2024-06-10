from .floor_entity import FloorEntity
from .wall_entity import WallEntity


class RPGMapLayer:
    width = 40
    height = 40

    floor_tiles: list[list[FloorEntity | None]]
    wall_tiles: list[list[WallEntity | None]]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.floor_tiles = [[None] * width] * height
        self.wall_tiles = [[None] * width] * height

    def get_tiles_at_position(
        self,
        x: int,
        y: int,
    ) -> tuple[FloorEntity | None, WallEntity | None]:
        return self.floor_tiles[x][y], self.wall_tiles[x][y]

    def get_tile_at_position_floor(self, x: int, y: int) -> FloorEntity | None:
        try:
            return self.floor_tiles[x][y]
        except IndexError:
            return None

    def get_tile_at_position_wall(self, x: int, y: int) -> WallEntity | None:
        try:
            return self.wall_tiles[x][y]
        except IndexError:
            return None

    def place_floor_at_position(self, x: int, y: int, tile: FloorEntity) -> None:
        self.floor_tiles[x][y] = tile

    def place_wall_at_position(self, x: int, y: int, tile: WallEntity) -> None:
        self.wall_tiles[x][y] = tile


class RPGMapBoard:
    layers: list[RPGMapLayer]

    def __init__(self, width: int = 40, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.layers = []
        self.layers.append(RPGMapLayer(width, height))

    def get_tiles_at_position(self, x: int, y: int, z: int) -> tuple[FloorEntity | None, WallEntity | None]:
        return self.layers[z].get_tiles_at_position(x, y)

    def get_all_tiles_at_position(self, x: int, y: int) -> list[tuple[FloorEntity | None, WallEntity | None]]:
        r: list[tuple[FloorEntity | None, WallEntity | None]] = []
        for layer in self.layers:
            r.append(layer.get_tiles_at_position(x, y))
        return r

    def place_floor_at_position_in_layer(self, x: int, y: int, z: int, tile: FloorEntity) -> None:
        self.layers[z].place_floor_at_position(x, y, tile)

    def place_wall_at_position_in_layer(self, x: int, y: int, z: int, tile: WallEntity) -> None:
        self.layers[z].place_wall_at_position(x, y, tile)

    def get_cell_neighbors_floor(self, x: int, y: int, z: int) -> list[FloorEntity | None]:
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

    def get_cell_neighbors_wall(self, x: int, y: int, z: int) -> list[WallEntity | None]:
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
