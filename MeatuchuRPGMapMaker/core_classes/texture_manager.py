import os

from PIL import Image

from MeatuchuRPGMapMaker import ROOTDIR

from . import FeatureManager
from .event_manager import EventManager


class TextureManager(FeatureManager):
    event_mgr: EventManager
    textures: dict[str, Image.Image]

    def __build__(self) -> None:
        self.textures = {}

    def load_texture(self, texture_name: str) -> Image.Image:
        self.log("DEBUG", f"Loading texture {texture_name}")
        texture_path = os.path.join(ROOTDIR, f"../resources/textures/{texture_name}.png")
        tex = open_image(texture_path)
        tex = tex.convert("L").convert("HSV")
        self.log("VERBOSE", f"Loaded texture {texture_name}")
        self.textures[texture_name] = tex
        return tex

    def get_texture(self, texture_name: str) -> Image.Image:
        return self.textures.get(texture_name, self.load_texture(texture_name))

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass


def open_image(image_path: str) -> Image.Image:
    return Image.open(image_path)  # pyright: ignore[reportUnknownMemberType]
