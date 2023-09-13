# Global app settings
from . import FeatureManager
from typing import Any

__settings_values__ = {
    "default": {"window": {"width": 1920, "height": 1080, "fullscreen_mode": 2}},
    "prod": {"window": {"fullscreen_mode": 2}},
    "beta": {"window": {"fullscreen_mode": 0}},
    "dev": {"window": {"width": 800, "height": 600, "fullscreen_mode": 0}},
}

settings_instance = 0


class SettingsManager(FeatureManager):
    session_settings = {}

    def __init__(self) -> None:
        super().__init__()

    def get_setting(self, group: str, key: str) -> Any:
        stage_config = __settings_values__.get(self.stage, {})
        default = __settings_values__["default"]
        v = stage_config.get(group, default[group]).get(key, default[group][key])
        self.logger.log(
            "INFO",
            f'Retrieved value "{v}" from setting "{key}" in group "{group}" for stage "{self.stage}"',
            self.name,
        )
        return v
