from typing import Any

from .UpdateEventClass import UpdateEvent


class EditSettingRequestEvent(UpdateEvent):
    # Fired when a window has been resized
    def __init__(self, group: str, key: str, value: Any = None) -> None:
        self.group = group
        self.key = key
        self.value = value
        super().__init__()
