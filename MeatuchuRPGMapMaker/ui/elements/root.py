import importlib
from tkinter import Tk as TkWindow

from ..scene_schema import SCENE_SCHEMA
from ..types import Margin, Padding
from .element import Element
from .text import Text


class Root(Element):
    ALLOW_CHILDREN: bool = True
    scene_name: str
    namespace: str | None
    ids: set[str]

    def __init__(self, window: TkWindow, scene_name: str, namespace: str | None = None) -> None:
        super().__init__(window=window, id="root", parent=None)
        self.margin = Margin(0)
        self.padding = Padding(0)
        self.scene_name = scene_name
        self.namespace = namespace
        self.ids = set()

    def render(self) -> None:
        pass

    def parse(self) -> None:
        scene_module = importlib.import_module(
            f"MeatuchuRPGMapMaker.ui.scenes{'.' + self.namespace if self.namespace else ''}"
        )
        scene_schema = getattr(scene_module, f"{self.scene_name}_scene_schema")
        assert scene_schema["type"] == "root"

        SCENE_SCHEMA.validate(scene_schema)
        self.__parse_elements(scene_schema)

    def __parse_elements(self, schema_element, parent: Element | None = None) -> None:
        parent = parent if parent else self

        new_element = None

        if schema_element["type"] == "root":
            new_element = self
        elif schema_element["type"] == "text":
            new_element = Text(self.window, parent, text=schema_element["text"], id=schema_element.get("id"))
            parent.add_child(new_element)

        if not new_element:
            raise ValueError(f"Unable to create scene element from schema element with type {schema_element["type"]}")

        if new_element.id:
            if new_element.id in self.ids:
                raise ValueError("Element IDs must be unique")
            self.ids.add(new_element.id)

        if schema_element.get("children"):
            for child_element in schema_element["children"]:
                self.__parse_elements(child_element, new_element)
