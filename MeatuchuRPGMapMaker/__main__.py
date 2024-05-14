from . import STAGE_STR, get_all_args
from .constants import DEPLOY_STAGE
from .core_classes.app_manager import AppManager
from .core_classes.entity_manager import EntityManager
from .core_classes.event_manager import EventManager
from .core_classes.export_manager import ExportManager
from .core_classes.input_manager import InputManager
from .core_classes.rendering_manager import RenderingManager
from .core_classes.settings_manager import SettingsManager
from .core_classes.texture_manager import TextureManager
from .core_classes.thread_manager import ThreadManager
from .core_classes.window_manager import WindowManager
from .events import AppShutDownEvent
from .logger import logger_factory

STAGE = DEPLOY_STAGE(STAGE_STR)

logger = logger_factory()
logger.open_log_file()
logger.log("VERBOSE", f"Starting App in Stage {STAGE_STR}")
logger.log("VERBOSE", f"Arguments: {get_all_args()}")

app = AppManager(
    EntityManager(),
    EventManager(),
    ExportManager(),
    InputManager(),
    RenderingManager(),
    SettingsManager(),
    TextureManager(),
    ThreadManager(),
    WindowManager(),
)

app.open_new_map()

try:
    app.activate_app()
except Exception as e:
    logger.handle_exception(e)
finally:
    logger.close_file()
    if not app.event_mgr.get_shutdown_status():
        app.event_mgr.queue_event(AppShutDownEvent())
