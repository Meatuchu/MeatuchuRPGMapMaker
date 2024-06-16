from . import STAGE_STR, get_all_args
from .constants import DEPLOY_STAGE
from .core_classes.app_manager import AppManager
from .events import AppShutDownEvent
from .logger import logger_factory

STAGE = DEPLOY_STAGE(STAGE_STR)

logger = logger_factory()
logger.open_log_file()
logger.log("VERBOSE", f"Starting App in Stage {STAGE_STR}")
logger.log("VERBOSE", f"Arguments: {get_all_args()}")

app = AppManager()

app.open_new_map()

try:
    app.activate_app()
except Exception as e:
    logger.handle_exception(e)
finally:
    logger.close_file()
    if not app.event_mgr.get_shutdown_status():
        app.event_mgr.queue_event(AppShutDownEvent())
