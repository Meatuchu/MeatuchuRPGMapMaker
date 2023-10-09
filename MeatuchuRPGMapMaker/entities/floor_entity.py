from .base_entity import BaseEntity


class FloorEntity(BaseEntity):
    id_name = "basic_floor_obj"
    str_name = "Basic Floor Object"

    def __init__(self) -> None:
        super().__init__()
