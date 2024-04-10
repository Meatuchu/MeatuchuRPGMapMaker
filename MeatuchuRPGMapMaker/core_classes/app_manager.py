import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..events import (
    AllThreadsDestroyedEvent,
    AppShutDownEvent,
    Event,
    SceneChangeRequestEvent,
    WindowFullscreenModeEditRequestEvent,
    WindowResizeRequestEvent,
)
from ..game.entities.board import RPGMapBoard
from ..ui.scenes.menu_scene import MenuScene
from . import FeatureManager
from .entity_manager import EntityManager
from .event_manager import EventManager
from .export_manager import ExportManager
from .input_manager import InputManager
from .rendering_manager import RenderingManager
from .settings_manager import SettingsManager
from .texture_manager import TextureManager
from .thread_manager import ThreadManager
from .window_manager import WindowManager


class AppState:
    state_queue: List[Tuple[str, Any]] = []

    # state
    app_active: bool
    active_board: Optional[RPGMapBoard]
    last_update_time: int = 0

    def __init__(self) -> None:
        self.app_active = False

    def set_tickrate(self, tickrate: int = 60) -> None:
        self.tickrate = tickrate
        self.tickgap = 1000000000 / tickrate

    def set_state(self, new_state: Tuple[str, Any]) -> None:
        key, val = new_state
        super().__setattr__(key, val)

    def queue_state_change(self, state_change: Tuple[str, Any]) -> None:
        self.state_queue.append(state_change)

    def process_state_queue(self) -> None:
        while len(self.state_queue):
            self.set_state(self.state_queue.pop(0))


class AppManager(FeatureManager):
    # dependencies
    entity_mgr: EntityManager
    event_mgr: EventManager
    export_mgr: ExportManager
    input_mgr: InputManager
    render_mgr: RenderingManager
    settings_mgr: SettingsManager
    texture_mgr: TextureManager
    thread_mgr: ThreadManager
    window_mgr: WindowManager

    # state
    state: AppState
    frame_counter: int
    start_time: float

    def __init__(
        self,
        entity_mgr: EntityManager,
        event_mgr: EventManager,
        export_mgr: ExportManager,
        input_mgr: InputManager,
        render_mgr: RenderingManager,
        settings_mgr: SettingsManager,
        texture_mgr: TextureManager,
        thread_mgr: ThreadManager,
        window_mgr: WindowManager,
    ) -> None:
        super().__init__()
        # Prepare app state
        self.register_event_manager(event_mgr)
        self.state = AppState()

        # Initialize metrics
        self.frame_counter = 0
        self.start_time = int(datetime.now().timestamp())

        # Register Features
        self.export_mgr = export_mgr
        self.entity_mgr = entity_mgr
        self.input_mgr = input_mgr
        self.render_mgr = render_mgr
        self.settings_mgr = settings_mgr
        self.texture_mgr = texture_mgr
        self.thread_mgr = thread_mgr
        self.window_mgr = window_mgr
        self.distribute_event_manager()
        self.state.set_tickrate(self.settings_mgr.get_setting("app", "tickrate"))

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        def shutdown(_: Event) -> None:
            return self.event_mgr.queue_event(AppShutDownEvent())

        self.event_mgr.register_subscription(AllThreadsDestroyedEvent, shutdown)
        pass

    def distribute_event_manager(self) -> None:
        self.entity_mgr.register_event_manager(self.event_mgr)
        self.export_mgr.register_event_manager(self.event_mgr)
        self.input_mgr.register_event_manager(self.event_mgr)
        self.render_mgr.register_event_manager(self.event_mgr)
        self.settings_mgr.register_event_manager(self.event_mgr)
        self.texture_mgr.register_event_manager(self.event_mgr)
        self.thread_mgr.register_event_manager(self.event_mgr)
        self.window_mgr.register_event_manager(self.event_mgr)

    def activate_app(self) -> None:
        self.state.app_active = True
        self.window_mgr.create_window()
        self.event_mgr.queue_event(
            WindowResizeRequestEvent(
                self.settings_mgr.get_setting("window", "width"),
                self.settings_mgr.get_setting("window", "height"),
            )
        )
        self.event_mgr.queue_event(
            WindowFullscreenModeEditRequestEvent(self.settings_mgr.get_setting("window", "fullscreen_mode"))
        )
        self.event_mgr.queue_event(SceneChangeRequestEvent(MenuScene))
        while True:
            while self.state.app_active:
                self.app_frame_process()

    def app_frame_process(self) -> None:
        cur_time = time.time_ns()
        if self.should_do_game_tick(cur_time):
            self.state.last_update_time = cur_time
            self.input_step(self.frame_counter)
            self.update_step(self.frame_counter)
        self.render_step(self.frame_counter)
        self.frame_counter += 1

    def should_do_game_tick(self, cur_time: int) -> bool:
        return (cur_time - self.state.last_update_time) >= self.state.tickgap

    def input_step(self, frame_number: int) -> None:
        self.event_mgr.queue_scheduled_events()
        self.input_mgr.input_step(self.frame_counter)
        self.entity_mgr.input_step(self.frame_counter)
        self.export_mgr.input_step(self.frame_counter)
        self.render_mgr.input_step(self.frame_counter)
        self.settings_mgr.input_step(self.frame_counter)
        self.texture_mgr.input_step(self.frame_counter)
        self.thread_mgr.input_step(self.frame_counter)
        self.window_mgr.input_step(self.frame_counter)
        self.event_mgr.input_step(self.frame_counter)
        return super().input_step(frame_number)

    def update_step(self, frame_number: int) -> None:
        self.event_mgr.queue_scheduled_events()
        self.input_mgr.update_step(self.frame_counter)
        self.entity_mgr.update_step(self.frame_counter)
        self.export_mgr.update_step(self.frame_counter)
        self.render_mgr.update_step(self.frame_counter)
        self.settings_mgr.update_step(self.frame_counter)
        self.texture_mgr.update_step(self.frame_counter)
        self.thread_mgr.update_step(self.frame_counter)
        self.window_mgr.update_step(self.frame_counter)
        self.event_mgr.update_step(self.frame_counter)
        return super().update_step(frame_number)

    def render_step(self, frame_number: int) -> None:
        self.event_mgr.queue_scheduled_events()
        self.input_mgr.render_step(self.frame_counter)
        self.entity_mgr.render_step(self.frame_counter)
        self.export_mgr.render_step(self.frame_counter)
        self.render_mgr.render_step(self.frame_counter)
        self.settings_mgr.render_step(self.frame_counter)
        self.texture_mgr.render_step(self.frame_counter)
        self.thread_mgr.render_step(self.frame_counter)
        self.window_mgr.render_step(self.frame_counter)
        self.event_mgr.render_step(self.frame_counter)
        return super().render_step(frame_number)

    def open_new_map(self) -> None:
        self.state.set_state(("active_board", RPGMapBoard()))

    def get_all_managers(self) -> Dict[str, FeatureManager]:
        mgrs: Dict[str, FeatureManager] = {}
        for attribute in dir(self):
            if attribute.endswith("mgr") and isinstance(self.__getattribute__(attribute), Callable):
                mgrs[attribute] = self.__getattribute__(attribute)
        return mgrs
