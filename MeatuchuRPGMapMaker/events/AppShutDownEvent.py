from .UpdateEvent import UpdateEvent


class AppShutDownEvent(UpdateEvent):
    # Fired before the app shuts down. This is the final event to be processed.
    # Subscribe to this event to be given a chance to perform cleanup
    pass
