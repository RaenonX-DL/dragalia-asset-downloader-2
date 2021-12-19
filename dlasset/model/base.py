"""JSON object model class."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

__all__ = ("JsonModel",)


# https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class JsonModel(ABC):
    """A data class that is based on a json object."""

    json_obj: dict[Any, Any] = field(hash=False)

    @abstractmethod
    def __post_init__(self) -> None:
        raise NotImplementedError()
