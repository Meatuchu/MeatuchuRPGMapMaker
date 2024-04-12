import os
from typing import Dict

from PIL import Image

from MeatuchuRPGMapMaker import ROOTDIR

from . import FeatureManager
from .event_manager import EventManager


class TextureManager(FeatureManager):
    event_mgr: EventManager
    textures: Dict[str, Image.Image]

    def __init__(self) -> None:
        self.textures = {}
        super().__init__()
        pass

    def load_texture(self, texture_name: str) -> Image.Image:
        self.log("DEBUG", f"Loading texture {texture_name}")
        r = os.path.join(ROOTDIR, f"../resources/textures/{texture_name}.png")
        tex = Image.open(r)
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
