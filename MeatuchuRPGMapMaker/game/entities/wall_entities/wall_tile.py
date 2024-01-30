from ..wall_entity import WallEntity


class WallTile(WallEntity):
    id_name: str = "wall_tile"
    str_name: str = "Wall Tile"

    def __init__(self) -> None:
        super().__init__()
