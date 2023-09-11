from .base_entity import BaseEntity


class WallTile(BaseEntity):
    id_name = "basic_wall_ent"
    str_name = "Basic Wall Tile"

    def __init__(self) -> None:
        super().__init__()
