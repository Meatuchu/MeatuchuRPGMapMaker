from unittest.mock import MagicMock, patch

from pytest import raises

from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.settings_manager import SettingsManager
from MeatuchuRPGMapMaker.events import EditSettingRequestEvent

mock_settings = {"any": {"window": {"width": 123, "height": 456}}}


def test_construction() -> None:
    assert SettingsManager()


@patch(
    "MeatuchuRPGMapMaker.core_classes.settings_manager.__settings_values__",
    mock_settings,
)
def test_settings_manager_defaults_correctly() -> None:
    settings_instance = SettingsManager()
    assert settings_instance.get_setting("window", "width") == 123


def test_register_event_manager() -> None:
    m = SettingsManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_manager(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()


def test_settings_manager_sets_new_settings() -> None:
    m = SettingsManager()
    m.set_setting("window", "title", "test_title")
    assert m.get_setting("window", "title") == "test_title"


@patch(
    "MeatuchuRPGMapMaker.core_classes.settings_manager.__settings_values__",
    mock_settings,
)
def test_settings_manager_overrwrites_settings() -> None:
    m = SettingsManager()
    assert m.get_setting("window", "width") == 123
    m.set_setting("window", "width", 456)
    assert m.get_setting("window", "width") == 456


@patch(
    "MeatuchuRPGMapMaker.core_classes.settings_manager.__settings_values__",
    mock_settings,
)
def test_settings_manager_missing_setting() -> None:
    settings_instance = SettingsManager()
    assert not settings_instance.get_setting("window", "made_up")


@patch(
    "MeatuchuRPGMapMaker.core_classes.settings_manager.__settings_values__",
    mock_settings,
)
def test_settings_manager_missing_setting_not_allow_none() -> None:
    settings_instance = SettingsManager()
    with raises(AttributeError):
        settings_instance.get_setting("window", "made_up", allow_none=False)


def test_handle_settings_edit_request_event() -> None:
    m = SettingsManager()
    e = EventManager()
    m.register_event_manager(e)
    m.subscribe_to_events()
    assert not m.get_setting("window", "title")
    e.queue_event(EditSettingRequestEvent("window", "title", "test_title"))
    e.queue_event = MagicMock()
    e.input_step(0)
    e.update_step(0)
    e.render_step(0)
    assert m.get_setting("window", "title") == "test_title"
    e.queue_event.assert_called()
