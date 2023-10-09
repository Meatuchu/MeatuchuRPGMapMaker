from PIL import Image, ImageTk
from typing import Dict
import os

from . import FeatureManager
from .event_manager import EventManager
from .. import ROOTDIR


class TextureManager(FeatureManager):
    event_mgr: EventManager
    textures: Dict[str, Image.Image]

    def __init__(self) -> None:
        self.textures = {}
        super().__init__()
        pass

    def load_texture(self, texture_name: str) -> None:
        r = os.path.join(ROOTDIR, f"../resources/textures/{texture_name}.png")
        tex = Image.open(r)
        tex = tex.convert("L").convert("HSV")
        self.textures[texture_name] = tex

    def get_texture(self, texture_name: str) -> Image.Image:
        return self.textures[texture_name]

    def register_event_mgr(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass
