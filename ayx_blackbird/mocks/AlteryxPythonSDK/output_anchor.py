"""Mock output anchor class definition."""
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .record_info import RecordInfo
    from .record_ref import RecordRef


class OutputAnchor:
    """Output anchor mock."""

    def __init__(self) -> None:
        self._is_closed: bool = False
        self._record_info: Optional["RecordInfo"] = None
        self.pushed_records: List["RecordRef"] = []

    def assert_close(self) -> None:
        """Assert the output anchor is closed."""
        assert self._is_closed

    def close(self) -> None:
        """Close the output anchor."""
        self._is_closed = True

    def init(self, record_info_out: "RecordInfo", sort_info_xml: str = "") -> bool:
        """Initialize the output anchor with record metadata."""
        self._record_info = record_info_out
        return True

    def output_record_count(self, final: bool) -> None:
        """Output the record count to Designer."""
        pass

    def push_record(self, record_ref: "RecordRef", no_auto_close: bool = False) -> bool:
        """Push a record downstream."""
        self.pushed_records.append(record_ref)
        return True

    def update_progress(self, percent: float) -> None:
        """Update progress."""
        pass
