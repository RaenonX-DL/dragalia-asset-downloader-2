"""Utility functions related to execution."""
import time
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from functools import wraps
from typing import Any, Callable, Hashable, Sequence, TypeVar, Union

from dlasset.log import init_log, log

__all__ = ("concurrent_run", "concurrent_run_no_return", "time_exec")

K = TypeVar("K", bound=Union[Hashable, None])
R = TypeVar("R")


def on_concurrency_start(log_dir: str) -> None:
    """Function to call on each concurrency start."""
    # Each process has a brand new logging factory
    init_log(log_dir)


def concurrent_run(
        fn: Callable[..., R],  # type: ignore
        args_list: Sequence[Sequence[Any]],
        log_dir: str, /,
        key_of_call: Callable[..., K]  # type: ignore
) -> dict[K, R]:
    """
    Run ``fn`` concurrently with different set of ``args``.

    If ``key_of_call`` is not ``None``, a ``dict`` where
    key is obtained from ``key_of_call`` and the value as the result will be returned.
    """
    results: dict[K, R] = {}

    def on_done(
            key_of_call: Callable[..., K],  # type: ignore
            args: Sequence[Any]
    ) -> Callable[[Future], None]:
        def inner(future: Future) -> None:
            results[key_of_call(*args)] = future.result()

        return inner

    with ProcessPoolExecutor(initializer=on_concurrency_start, initargs=(log_dir,)) as executor:
        futures: list[Future] = []
        for args in args_list:
            future = executor.submit(fn, *args)

            if key_of_call:
                future.add_done_callback(on_done(key_of_call, args))

        as_completed(futures)

    return results


def concurrent_run_no_return(
        fn: Callable[..., R],
        args_list: Sequence[Sequence[Any]],
        log_dir: str
) -> None:  # type: ignore
    """
    Run ``fn`` concurrently with different set of ``args``.

    Does not return result.
    """

    def key_of_call(*_: Any, **__: Any) -> None:
        return None

    concurrent_run(fn, args_list, log_dir, key_of_call=key_of_call)


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
