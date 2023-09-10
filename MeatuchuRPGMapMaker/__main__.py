from . import STAGE
from .core_classes.settings_manager import SettingsManager
from .core_classes.window_manager import WindowManager

window_manager = WindowManager()
settings = SettingsManager()


window_manager.set_window_size(
    settings.get_setting("window", "width"), settings.get_setting("window", "height")
)
window_manager.set_fullscreen_mode(0)
window_manager.activate_window()
print(STAGE)
print("executed successfully")
