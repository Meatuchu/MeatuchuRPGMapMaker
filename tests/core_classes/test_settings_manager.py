from unittest.mock import patch
from MeatuchuRPGMapMaker.core_classes.settings_manager import SettingsManager


mock_settings = {"default": {"window": {"width": 123, "height": 456}}}


def test_construction() -> None:
    assert SettingsManager()


@patch(
    "MeatuchuRPGMapMaker.core_classes.settings_manager.__settings_values__",
    mock_settings,
)
def test_settings_manager_defaults_correctly() -> None:
    settings_instance = SettingsManager()
    assert settings_instance.get_setting("window", "width") == 123
