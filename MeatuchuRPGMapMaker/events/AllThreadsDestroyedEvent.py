from .UpdateEvent import UpdateEvent


class AllThreadsDestroyedEvent(UpdateEvent):
    # Fired when ThreadManager destroys its final thread.
    pass