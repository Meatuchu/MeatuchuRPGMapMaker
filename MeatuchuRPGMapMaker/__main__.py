from .core_classes.settings_manager import SettingsManager
from .core_classes.entity_manager import EntityManager
from .core_classes.window_manager import WindowManager
from .logger import logger_factory

logger = logger_factory()
window_manager = WindowManager()
entity_manager = EntityManager()
settings = SettingsManager()

window_manager.set_window_size(
    settings.get_setting("window", "width"), settings.get_setting("window", "height")
)
window_manager.set_fullscreen_mode(0)
window_manager.activate_window()
