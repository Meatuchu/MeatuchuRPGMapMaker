import threading
from typing import Dict, Callable, Tuple, Any

from . import FeatureManager
from .event_manager import EventManager
from .events import (
    AllThreadsDestroyedEvent,
    NewThreadEvent,
    NewThreadRequestEvent,
    DestroyThreadEvent,
    DestroyThreadRequestEvent,
)


class ThreadManager(FeatureManager):
    _threads: Dict[str, Tuple[str, threading.Thread]]
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

    def create_thread(self, event: NewThreadRequestEvent) -> None:
        thread_name: str = event.kwargs["thread_name"]
        thread_target: Callable[..., None] = event.kwargs["thread_target"]
        owner_id: str = event.kwargs["owner_id"]

        self.log("DEBUG", f"Recieved request to create thread {thread_name}")

        if self._threads.get(thread_name):
            raise RuntimeError(f"thread {thread_name} already exists!")

        new_thread = threading.Thread(target=thread_target)
        new_thread.daemon = True
        self._threads[thread_name] = (owner_id, new_thread)
        new_thread.start()

        self.log("DEBUG", f"Created new thread {thread_name}")

        self.event_mgr.queue_event(NewThreadEvent(thread_name))
        pass

    def destroy_thread(self, event: DestroyThreadRequestEvent) -> None:
        thread_name: str = event.kwargs["thread_name"]
        owner_id: str = event.kwargs["owner_id"]
        self.log("DEBUG", f"Recieved request to destroy thread {thread_name}")
        target = self._threads.get(thread_name)
        if not target:
            return

        true_owner, thread = target

        if owner_id != true_owner:
            return

        thread.join()
        self.log("DEBUG", f"(fake) Destroyed thread {thread_name}")
        del self._threads[thread_name]
        self.event_mgr.queue_event(DestroyThreadEvent(thread_name))
        if not self._threads:
            self.event_mgr.queue_event(AllThreadsDestroyedEvent())
        pass
