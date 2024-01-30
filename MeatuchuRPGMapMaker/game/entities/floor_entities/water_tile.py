from ..floor_entity import FloorEntity


class WaterTile(FloorEntity):
    id_name = "water_tile"
    str_name = "Water Tile"

    def __init__(self) -> None:
        super().__init__()
