class DuplicateThreadError(RuntimeError):
    def __init__(self, thread: str, owner_id: str) -> None:
        super().__init__(f"Duplicate thread {thread} was created by {owner_id}")


class DuplicateSceneElementError(RuntimeError):
    def __init__(self, element: str, scene: str) -> None:
        super().__init__(f"Duplicate element {element} added to scene {scene}!")


class ElementCreatedWithoutWindowError(ValueError):
    def __init__(self, ename: str) -> None:
        super().__init__(f"Element {ename} was instantiated without a window!")


class ElementNotNamedError(TypeError):
    def __init__(self, eclass: str) -> None:
        super().__init__(f"Element {eclass} instantiated without name!")


class DuplicateWindowError(RuntimeError):
    def __init__(self, window_name: str) -> None:
        super().__init__(f"Window {window_name} already exists!")


class WindowNotFoundError(RuntimeError):
    def __init__(self, window_name: str) -> None:
        super().__init__(f"Couldn't find window {window_name}! Is there something wrong with the window create thread?")


class WindowNotExistError(KeyError):
    def __init__(self, window_name: str) -> None:
        super().__init__(f"Window {window_name} does not exist!")
