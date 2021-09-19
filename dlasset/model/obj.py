"""JSON object model class."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

__all__ = ("JsonModel",)


@dataclass
class JsonModel(ABC):
    """A data class that is based on a json object."""

    json_obj: dict[Any, Any]

    @abstractmethod
    def __post_init__(self) -> None:
        raise NotImplementedError()
