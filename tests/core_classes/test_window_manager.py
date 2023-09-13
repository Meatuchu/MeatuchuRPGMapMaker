# pyright: reportPrivateUsage=false
from typing import Any
from unittest.mock import MagicMock, call, patch
from pytest import raises
from MeatuchuRPGMapMaker.core_classes.window_manager import WindowManager


# helper mock
class mock_tk_def:
    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except:
            super().__setattr__(__name, MagicMock())
            return super().__getattribute__(__name)

    def __init__(self) -> None:
        pass


# tests
def test_construction() -> None:
    assert WindowManager()


def test_window_already_exists() -> None:
    w = WindowManager()
    w.create_window("test")
    with raises(KeyError):
        w.create_window("test")


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_window_activate(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = mock_tk_def()
    w = WindowManager()
    w.activate_window()
    w.create_window("side")
    w.activate_window("side")

    mock_Tk.return_value.mainloop.assert_has_calls([call(), call()])


@patch("MeatuchuRPGMapMaker.core_classes.window_manager.tk.Tk")
def test_window_set_size(mock_Tk: MagicMock) -> None:
    mock_Tk.return_value = mock_tk_def()
    w = WindowManager()
    w.set_window_size(200, 200)
    w.create_window("side")
    w.set_window_size(300, 300, "side")
    mock_Tk.return_value.geometry.assert_has_calls([call("200x200"), call("300x300")])
