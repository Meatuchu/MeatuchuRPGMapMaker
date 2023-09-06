# Global app settings
from ..constants import DEPLOY_STAGE
from typing import Any

__settings_values__ = {
    "default": {"window": {"width": 1920, "height": 1080, "fullscreen_mode": 2}},
    "prod": {"window": {"fullscreen_mode": 2}},
    "beta": {"window": {"fullscreen_mode": 0}},
    "dev": {"window": {"width": 800, "height": 600, "fullscreen_mode": 0}},
}

settings_instance = 0


class SettingsManager:
    stage = "prod"
    session_settings = {}

    def __init__(self, stage: str = "prod") -> None:
        DEPLOY_STAGE(stage)
        self.stage = stage

    def get_setting(self, group: str, key: str) -> Any:
        stage_config = __settings_values__.get(self.stage, {})
        default = __settings_values__["default"]
        return stage_config.get(group, default[group]).get(key, default[group][key])
