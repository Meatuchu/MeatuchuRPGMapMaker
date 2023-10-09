from ..floor_entity import FloorEntity


class FloorTile(FloorEntity):
    id_name = "floor_tile"
    str_name = "Floor Tile"

    def __init__(self) -> None:
        super().__init__()
