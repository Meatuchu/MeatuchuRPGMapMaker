from typing import Any

from .UpdateEventClass import UpdateEvent


class SettingEditedEvent(UpdateEvent):
    # Fired when a setting has been changed
    def __init__(self, group: str, key: str, value: Any) -> None:
        self.group = group
        self.key = key
        self.value = value
        super().__init__()
