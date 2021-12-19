"""Export result object."""
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .types import MonoBehaviourTree


@dataclass
class ExportResult:
    """Export result object."""

    tree: Optional[list["MonoBehaviourTree"]] = field(default=None)

    exported_paths: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Force replacing backslash `\` with slash `/`
        self.exported_paths = [export_path.replace("\\", "/") for export_path in self.exported_paths]
