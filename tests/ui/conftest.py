from typing import Any, Generator

import pytest

from MeatuchuRPGMapMaker.ui.scene import Scene


@pytest.fixture(autouse=True)
def before_after_each_test() -> Generator[None, Any, None]:
    q = []
    Scene.inject_queue_event(lambda event: q.append(event))
    Scene.inject_subscribe_to_event(lambda event, fn: "")
    Scene.inject_unsubscribe_from_event(lambda id: None)
    yield
