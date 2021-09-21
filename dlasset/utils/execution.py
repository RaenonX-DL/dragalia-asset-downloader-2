"""Utility functions related to execution."""
import sys
import time
from concurrent.futures import Future, ProcessPoolExecutor
from functools import wraps
from typing import Any, Callable, Hashable, Sequence, TypeVar, Union

from dlasset.log import init_log, log
from .misc import split_chunks

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
        log_dir: str, *,
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
            try:
                results[key_of_call(*args)] = future.result()
            except Exception as ex:
                log("ERROR", ex, exc_info=True)
                raise ex

        return inner

    # Memory in an executor will only release after the executor has shutdown (exiting the `with` statement)
    # Therefore splitting args list (tasks) into chunks
    for args_chunk in split_chunks(args_list, 1000):
        with ProcessPoolExecutor(initializer=on_concurrency_start, initargs=(log_dir,)) as executor:
            futures: list[Future] = []
            for args in args_chunk:
                future = executor.submit(fn, *args)

                if key_of_call:
                    future.add_done_callback(on_done(key_of_call, args))

                futures.append(future)

        exceptions = [future.exception() for future in futures if future.exception()]
        if error_count := len(exceptions):
            log("ERROR", f"{error_count} of {len(futures)} concurrent tasks have error.")
            log("ERROR", "-" * 20)
            for exception in exceptions:
                log("ERROR", f"{exception.__class__.__name__}: {exception}")
            sys.exit(1)

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
