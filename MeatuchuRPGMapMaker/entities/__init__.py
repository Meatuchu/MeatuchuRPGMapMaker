class BaseEntity:
    id: str

    def __init__(self) -> None:
        pass

    def set_id(self, id: str) -> None:
        if not id:
            raise ValueError(f"invalid Id {id} provided to {self.__class__}")
        self.id = id


class FloorTile(BaseEntity):
    def __init__(self) -> None:
        super().__init__()


class WallTile(BaseEntity):
    def __init__(self) -> None:
        super().__init__()
