# Global app settings
from typing import Any

from . import FeatureManager
from .event_manager import EventManager

__settings_values__ = {
    "default": {
        "window": {"width": 1920, "height": 1080, "fullscreen_mode": 2, "name": "test"},
        "app": {
            "tickrate": 60,
        },
    },
    "prod": {
        "window": {
            "fullscreen_mode": 2,
        },
    },
    "beta": {
        "window": {
            "fullscreen_mode": 0,
        }
    },
    "dev": {
        "window": {
            "width": 800,
            "height": 600,
            "fullscreen_mode": 0,
        },
    },
}

settings_instance = 0


class SettingsManager(FeatureManager):
    event_mgr: EventManager
    session_settings = {}

    def __init__(self) -> None:
        super().__init__()

    def get_setting(self, group: str, key: str) -> Any:
        stage_config = __settings_values__.get(self.stage.value, {})
        default = __settings_values__["default"]
        v = stage_config.get(group, default[group]).get(key, default[group][key])
        self.log(
            "INFO",
            f'Retrieved value {f"{v}" if type(v) is str else v} from setting "{key}" in group "{group}" for stage "{self.stage}"',
        )
        return v

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass
