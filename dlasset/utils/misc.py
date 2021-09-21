"""Miscellaneous utility functions."""
from typing import Any, Generator, Sequence

__all__ = ("split_chunks",)


def split_chunks(seq: Sequence[Any], size: int) -> Generator[Sequence[Any], None, None]:
    """Yields items in ``seq`` in chunks of ``size``."""
    for i in range(0, len(seq), size):
        yield seq[i:i + size]
