from .base_entity import BaseEntity


class FloorTile(BaseEntity):
    id_name = "basic_floor_ent"
    str_name = "Basic Floor Tile"

    def __init__(self) -> None:
        super().__init__()
