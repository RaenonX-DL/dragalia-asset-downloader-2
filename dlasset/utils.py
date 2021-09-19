"""Various utility functions."""
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import wraps
from typing import Any, Callable, Sequence, TypeVar

from .log import log

__all__ = ("concurrent_run", "time_exec")


def concurrent_run(fn: Callable, args_list: Sequence[Sequence[Any]]) -> None:
    """Run ``fn`` concurrently with different set of ``args``."""
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fn, *args) for args in args_list]
        as_completed(futures)


FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def time_exec(title: str) -> Callable[[FuncT], Any]:
    """Time a function execution and log it."""
    def decorator(fn: FuncT) -> Any:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _start = time.time()
            ret = fn(*args, **kwargs)
            log("INFO", f"{title} completed in {time.time() - _start:.3f} secs")
            return ret

        return wrapper

    return decorator
