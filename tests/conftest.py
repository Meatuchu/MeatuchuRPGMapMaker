from typing import Any, Generator

import pytest

from MeatuchuRPGMapMaker.core_classes.app_manager import AppManager
from MeatuchuRPGMapMaker.core_classes.entity_manager import EntityManager
from MeatuchuRPGMapMaker.core_classes.event_manager import EventManager
from MeatuchuRPGMapMaker.core_classes.export_manager import ExportManager
from MeatuchuRPGMapMaker.core_classes.input_manager import InputManager
from MeatuchuRPGMapMaker.core_classes.rendering_manager import RenderingManager
from MeatuchuRPGMapMaker.core_classes.settings_manager import SettingsManager
from MeatuchuRPGMapMaker.core_classes.texture_manager import TextureManager
from MeatuchuRPGMapMaker.core_classes.thread_manager import ThreadManager
from MeatuchuRPGMapMaker.core_classes.window_manager import WindowManager


@pytest.fixture(autouse=True)
def before_after_each_test() -> Generator[None, Any, None]:
    # Before each test
    AppManager.instance = None
    EntityManager.instance = None
    EventManager.instance = None
    ExportManager.instance = None
    InputManager.instance = None
    RenderingManager.instance = None
    SettingsManager.instance = None
    TextureManager.instance = None
    ThreadManager.instance = None
    WindowManager.instance = None

    # Run the test
    yield

    # After each test
    AppManager.instance = None
    EntityManager.instance = None
    EventManager.instance = None
    ExportManager.instance = None
    InputManager.instance = None
    RenderingManager.instance = None
    SettingsManager.instance = None
    TextureManager.instance = None
    ThreadManager.instance = None
    WindowManager.instance = None
