"""Mock record ref class definition."""
from typing import Any, Dict


class RecordRef:
    """Record ref mock."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def set_field(self, name: str, value: Any) -> None:
        self._data[name] = value


