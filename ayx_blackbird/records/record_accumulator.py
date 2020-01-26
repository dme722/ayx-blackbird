"""Record container definition."""
from typing import Optional

from .parsed_record_container import ParsedRecordContainer
from .raw_record_container import RawRecordContainer
from ..proxies import RecordProxy


class RecordAccumulator:
    __slots__ = ["raw_record_container", "parsed_record_container"]

    def __init__(
        self,
        raw_record_container: Optional[RawRecordContainer] = None,
        parsed_record_container: Optional[ParsedRecordContainer] = None,
    ):
        self.raw_record_container = raw_record_container
        self.parsed_record_container = parsed_record_container

    def add_record(self, record: RecordProxy) -> None:
        if self.raw_record_container:
            self.raw_record_container.add_record(record)

        if self.parsed_record_container:
            self.parsed_record_container.add_record(record)

    def clear_records(self) -> None:
        if self.raw_record_container:
            self.raw_record_container.clear_records()

        if self.parsed_record_container:
            self.parsed_record_container.clear_records()
