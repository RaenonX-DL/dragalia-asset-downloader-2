"""Typings for exporting."""
from typing import TypedDict

__all__ = ("TaskEntry",)


class SubTaskEntry(TypedDict):
    """Subtask entry of an updated file index."""

    name: str
    paths: list[str]


class TaskEntry(TypedDict):
    """Task entry of an updated file index."""

    name: str
    subtasks: list[SubTaskEntry]
