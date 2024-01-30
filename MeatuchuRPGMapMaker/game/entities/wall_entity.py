from .base_entity import BaseEntity


class WallEntity(BaseEntity):
    id_name = "basic_wall_obj"
    str_name = "Basic Wall Object"

    def __init__(self) -> None:
        super().__init__()
