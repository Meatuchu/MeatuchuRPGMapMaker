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

    def pre_render(self, frame_number: int) -> None:
        pass

    def render(self, frame_number: int) -> None:
        pass

    def post_render(self, frame_number: int) -> None:
        pass
