class BaseEntity:
    id_name = "ent"
    str_name = "Entity"

    ent_id: str

    def __init__(self) -> None:
        pass

    def set_id(self, id: str) -> None:
        if not id:
            raise ValueError(f"invalid Id {id} provided to {self.__class__}")
        self.id = id


class FloorTile(BaseEntity):
    id_name = "basic_floor_ent"
    str_name = "Basic Floor Tile"

    def __init__(self) -> None:
        super().__init__()


class WallTile(BaseEntity):
    id_name = "basic_wall_ent"
    str_name = "Basic Wall Tile"

    def __init__(self) -> None:
        super().__init__()
