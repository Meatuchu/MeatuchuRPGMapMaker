# pyright: reportPrivateUsage=false
from unittest.mock import MagicMock, patch

from pytest import raises
from MeatuchuRPGMapMaker.core_classes.thread_manager import ThreadManager
from typing import cast


def test_construction() -> None:
    assert ThreadManager()


def test_register_entity_manager() -> None:
    m = ThreadManager()
    event_mgr = MagicMock()
    o = m.subscribe_to_events
    m.subscribe_to_events = MagicMock(side_effect=o)
    m.register_event_mgr(event_mgr)
    m.event_mgr = event_mgr
    m.subscribe_to_events.assert_called_once()


@patch("MeatuchuRPGMapMaker.core_classes.thread_manager.threading.Thread")
def test_create_thread(mock_Thread_def: MagicMock) -> None:
    m = ThreadManager()
    m.register_event_mgr(MagicMock())
    m.event_mgr = cast(MagicMock, m.event_mgr)

    thread_instance = MagicMock()
    thread_instance.start = MagicMock()
    mock_Thread_def.return_value = thread_instance
    thread_target = MagicMock()

    m.create_thread("test_thread", thread_target, "unittest")
    assert m._threads["test_thread"] == ("unittest", thread_instance)
    assert thread_instance.daemon is True
    thread_instance.start.assert_called_once()
    m.event_mgr.queue_event.assert_called_once()


@patch("MeatuchuRPGMapMaker.core_classes.thread_manager.threading.Thread")
def test_create_thread_already_exists(mock_Thread_def: MagicMock) -> None:
    m = ThreadManager()
    m.register_event_mgr(MagicMock())
    m.event_mgr = cast(MagicMock, m.event_mgr)

    thread_instance = MagicMock()
    thread_instance.start = MagicMock()
    mock_Thread_def.return_value = thread_instance
    thread_target = MagicMock()

    m.create_thread("test_thread", thread_target, "unittest")
    with raises(RuntimeError):
        m.create_thread("test_thread", thread_target, "unittest")


@patch("MeatuchuRPGMapMaker.core_classes.thread_manager.threading.Thread")
def test_destroy_thread(mock_Thread_def: MagicMock) -> None:
    m = ThreadManager()
    m.register_event_mgr(MagicMock())
    m.event_mgr = cast(MagicMock, m.event_mgr)

    thread_instance = MagicMock()
    thread_instance.start = MagicMock()
    mock_Thread_def.return_value = thread_instance
    thread_target = MagicMock()

    m.create_thread("test_thread", thread_target, "unittest")
    m.destroy_thread("test_thread", "unittest")
    assert not m._threads.get("test_thread")


@patch("MeatuchuRPGMapMaker.core_classes.thread_manager.threading.Thread")
def test_destroy_thread_not_owner(mock_Thread_def: MagicMock) -> None:
    m = ThreadManager()
    m.register_event_mgr(MagicMock())
    m.event_mgr = cast(MagicMock, m.event_mgr)

    thread_instance = MagicMock()
    thread_instance.start = MagicMock()
    mock_Thread_def.return_value = thread_instance
    thread_target = MagicMock()

    m.create_thread("test_thread", thread_target, "unittest")
    m.destroy_thread("test_thread", "someone else")
    assert m._threads.get("test_thread")


def test_destroy_thread_not_exist() -> None:
    m = ThreadManager()
    m.register_event_mgr(MagicMock())
    m.event_mgr = cast(MagicMock, m.event_mgr)

    m.destroy_thread("test_thread", "unittest")
