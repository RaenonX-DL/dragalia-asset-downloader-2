"""Various utility functions."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, Sequence

__all__ = ("concurrent_run",)


def concurrent_run(fn: Callable, args_list: Sequence[Sequence[Any]]) -> None:
    """Run ``fn`` concurrently with different set of ``args``."""
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fn, *args) for args in args_list]
        as_completed(futures)
