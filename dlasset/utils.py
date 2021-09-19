"""Various utility functions."""
import time
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from functools import wraps
from typing import Any, Callable, Hashable, Optional, Sequence, TypeVar

from .log import log

__all__ = ("concurrent_run", "time_exec")

K = TypeVar("K", bound=Hashable)
R = TypeVar("R")


def concurrent_run(
        fn: Callable[[..., Any], R],  # type: ignore
        args_list: Sequence[Sequence[Any]], /,
        key_of_call: Optional[Callable[[..., Any], K]] = None  # type: ignore
) -> Optional[dict[K, R]]:
    """
    Run ``fn`` concurrently with different set of ``args``.

    If ``key_of_call`` is not ``None``, a ``dict`` where
    key is obtained from ``key_of_call`` and the value as the result will be returned.
    """
    results: dict[K, R] = {}

    def on_done(key_of_call: Callable[[Any, ...], K], args: Sequence[Any]) -> Callable[[Future], None]:  # type: ignore
        def inner(future: Future) -> None:
            results[key_of_call(*args)] = future.result()

        return inner

    with ProcessPoolExecutor() as executor:
        futures: list[Future] = []
        for args in args_list:
            future = executor.submit(fn, *args)

            if key_of_call:
                future.add_done_callback(on_done(key_of_call, args))

        as_completed(futures)

    if key_of_call:
        return results

    return None


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
