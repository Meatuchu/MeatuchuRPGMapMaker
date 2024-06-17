import threading
import traceback
from typing import Any, Callable

from MeatuchuRPGMapMaker.events import (
    AllThreadsDestroyedEvent,
    DestroyThreadEvent,
    DestroyThreadRequestEvent,
    NewThreadEvent,
    NewThreadRequestEvent,
    ThreadErrorEvent,
)
from MeatuchuRPGMapMaker.exceptions import DuplicateThreadError

from . import FeatureManager
from .event_manager import EventManager


class ThreadManager(FeatureManager):
    _threads: dict[str, tuple[str, threading.Thread]]
    event_mgr: EventManager

    def __init__(self) -> None:
        self._threads = {}
        super().__init__()

    def register_event_manager(self, event_mgr: EventManager) -> None:
        self.event_mgr = event_mgr
        self.subscribe_to_events()

    def subscribe_to_events(self) -> None:
        self.event_mgr.register_subscription(NewThreadRequestEvent, self.create_thread)
        self.event_mgr.register_subscription(DestroyThreadRequestEvent, self.destroy_thread)
        self.event_mgr.register_subscription(ThreadErrorEvent, self.log_thread_error)

    def create_thread(self, event: NewThreadRequestEvent) -> None:
        thread_name = event.thread_name
        owner_id: str = event.owner_id
        thread_target = self._thread_wrapper(thread_name, event.thread_target, owner_id)

        self.log("DEBUG", f"Recieved request to create thread {thread_name}")

        if self._threads.get(thread_name):
            raise DuplicateThreadError(thread_name, owner_id)

        new_thread = threading.Thread(target=thread_target)
        new_thread.daemon = True
        self._threads[thread_name] = (owner_id, new_thread)
        new_thread.start()

        self.log("DEBUG", f"Created new thread {thread_name}")

        self.event_mgr.queue_event(NewThreadEvent(thread_name))

    def destroy_thread(self, event: DestroyThreadRequestEvent) -> None:
        thread_name = event.thread_name
        owner_id = event.owner_id
        self.log("DEBUG", f"Recieved request to destroy thread {thread_name}")
        target = self._threads.get(thread_name)
        if not target:
            return

        true_owner, thread = target

        if owner_id != true_owner:
            return

        thread.join()
        self.log("DEBUG", f"Joined thread {thread_name}")
        del self._threads[thread_name]
        self.event_mgr.queue_event(DestroyThreadEvent(thread_name))
        if not self._threads:
            self.event_mgr.queue_event(AllThreadsDestroyedEvent())

    def log_thread_error(self, event: ThreadErrorEvent) -> None:
        self.log("ERROR", f'{event.exception.__class__.__name__} in thread "{event.thread_name}"!')
        self.log("ERROR", f"Exception Message -\n{type(event.exception)}\n{str(event.exception)}")
        self.log("ERROR", f"Exception Trace -\n{traceback.format_exc()}")

    def _thread_wrapper(self, name: str, target: Callable[..., Any], owner_id: str) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                target(*args, **kwargs)
            except Exception as e:
                self.event_mgr.queue_event(ThreadErrorEvent(name, owner_id, e))

        return wrapper
