from functools import wraps
from typing import Callable, Any
from datetime import datetime


def debounce(
    debounce_time: float = 1,
) -> Callable[..., Any]:
    def decorator(func_to_wrap: Callable[..., Any]) -> Callable[..., Any]:
        class Debouncer:
            last_call_time: float = 0
            last_return: Any = None

        @wraps(func_to_wrap)
        def debounced_function(*args: Any, **kwargs: Any) -> Any:
            cur = datetime.now().timestamp()
            __wrapped__ = func_to_wrap
            if Debouncer.last_call_time + debounce_time < cur:
                Debouncer.last_call_time = cur
                Debouncer.last_return = func_to_wrap(*args, **kwargs)
            return Debouncer.last_return

        return debounced_function

    return decorator
