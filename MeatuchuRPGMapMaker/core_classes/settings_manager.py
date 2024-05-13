# Global app settings
from typing import Any, Dict, Literal

from . import FeatureManager
from .event_manager import EventManager

STAGE_CONFIG_TYPE = Dict[str, Dict[str, Any]]
GROUP_CONFIG_TYPE = Dict[str, Any]


__settings_values__: Dict[Literal["any", "prod", "beta", "dev"], STAGE_CONFIG_TYPE] = {
    "any": {
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
    session_settings: GROUP_CONFIG_TYPE = {}

    def __init__(self) -> None:
        super().__init__()

    def get_setting(self, group: str, key: str, default: Any = None, allow_none: bool = True) -> Any:
        session_value = self.session_settings.get(group, {}).get(key)
        if session_value:
            return session_value

        fallback_value = __settings_values__["any"].get(group, {}).get(key, default)

        stage_config = __settings_values__.get(self.stage.value, {})
        value = stage_config.get(group, {}).get(key, fallback_value)

        self.log(
            "DEBUG",
            f'Retrieved value {f"{value}" if isinstance(value, str) else value} from setting "{key}" in group "{group}" for stage "{self.stage}"',
        )

        if value is None and not allow_none:
            raise AttributeError(f"Setting {key} in group {group} not found")

        return value

    def set_setting(self, group: str, key: str, value: Any) -> None:
        self.session_settings[group] = self.session_settings.get(group, {}) or {}
        self.session_settings[group][key] = value
        self.log(
            "DEBUG",
            f'Set value {f"{value}" if isinstance(value, str) else value} for setting "{key}" in group "{group}"',
        )

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        pass
