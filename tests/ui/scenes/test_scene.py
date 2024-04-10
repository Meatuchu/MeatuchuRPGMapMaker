from typing import List
from unittest.mock import MagicMock

from MeatuchuRPGMapMaker.events import Event
from MeatuchuRPGMapMaker.ui.scenes.scene import Scene


def test_construction() -> None:
    q: List[Event] = []
    assert Scene(MagicMock(), q.append)
