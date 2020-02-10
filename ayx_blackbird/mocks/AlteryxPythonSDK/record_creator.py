"""Mock record creator class definition."""
from typing import Any, TYPE_CHECKING

from .record_ref import RecordRef

if TYPE_CHECKING:
    from .record_info import RecordInfo


class RecordCreator:
    """Record Creator mock."""

    def __init__(self, record_info: "RecordInfo") -> None:
        """Construct a record creator."""
        self.record_ref = RecordRef(record_info)
        self._record_info = record_info

    def finalize_record(self) -> RecordRef:
        """Finalize a record ref."""
        return self.record_ref

    def reset(self, var_data_size: int = 0) -> None:
        """Reset the creator."""
        self.record_ref = RecordRef(self._record_info)

    def set_field(self, name: str, value: Any) -> None:
        """Set a field in the underlying record ref."""
        self.record_ref.set_field(name, value)
