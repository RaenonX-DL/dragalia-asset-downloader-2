"""Utility function for exporting."""
import json
from typing import Any, Optional

__all__ = ("export_json",)


def round_floats(obj: Any) -> Any:
    """Round the ``float`` in ``obj``."""
    if isinstance(obj, float):
        return float(format(obj, ".7g"))

    if isinstance(obj, dict):
        return {k: round_floats(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [round_floats(x) for x in obj]

    return obj


def export_json(export_path: str, obj: Any, *, separators: Optional[tuple[str, str]] = None) -> None:
    """
    Export the object ``obj`` to ``export_path``.

    It was tested that the solutions below are slower:

    >>> with open(export_path, "w+", encoding="utf-8") as f:
    >>>     f.write(json.dumps(
    >>>         json.loads(
    >>>             json.dumps(obj),
    >>>             parse_float=lambda x: f"{float(x):.9g}"
    >>>         )
    >>>     ))

    The solution above was about on par.

    >>> with open(export_path, "w+", encoding="utf-8") as f:
    >>>     json.dump(round_floats(obj), f)

    The solution above is about 3x slower.

    >>> with open(export_path, "w+", encoding="utf-8") as f:
    >>>     json.dump(
    >>>         json.loads(json.dumps(obj), parse_float=lambda x: f"{float(x):.9g}"),
    >>>         f,
    >>>     )

    The solution above is about 3x slower.
    """
    with open(export_path, "w+", encoding="utf-8") as f:
        f.write(json.dumps(round_floats(obj), ensure_ascii=False, indent=2, separators=separators))
