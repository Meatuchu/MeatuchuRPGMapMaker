from PIL import Image, ImageTk
from typing import Dict
import os

from . import FeatureManager
from .. import ROOTDIR


class TextureManager(FeatureManager):
    textures: Dict[str, Image.Image]

    def __init__(self) -> None:
        self.textures = {}
        super().__init__()
        pass

    def load_texture(self, texture_name: str) -> None:
        r = os.path.join(ROOTDIR, f"resources/textures/{texture_name}.png")
        tex = Image.open(r)
        tex = tex.convert("L").convert("HSV")
        self.textures[texture_name] = tex

    def get_texture(self, texture_name: str) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(self.textures[texture_name])
