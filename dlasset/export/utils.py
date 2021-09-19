"""Various utility functions."""
from .model import ExportInfo
from .types import ExportInfoPathDict

__all__ = ("get_export_info_path_dict",)


def get_export_info_path_dict(export_info_list: list[ExportInfo]) -> ExportInfoPathDict:
    """Get a :class:`dict` which key is the path ID; value is the corresponding :class:`ExportInfo`."""
    return {export_info.obj.path_id: export_info for export_info in export_info_list}
