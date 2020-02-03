"""Mock output anchor class definition."""
from .record_info import RecordInfo
from .record_ref import RecordRef


class OutputAnchor:
    """Output anchor mock."""

    def assert_close(self) -> None:
        pass

    def close(self) -> None:
        pass

    def init(self, record_info_out: RecordInfo, sort_info_xml: str = "") -> bool:
        pass

    def output_record_count(self, final: bool) -> None:
        pass

    def push_record(self, record_ref: RecordRef, no_auto_close: bool = False) -> bool:
        pass

    def update_progress(self, percent: float) -> None:
        pass
