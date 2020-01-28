"""BaseRecordContainer class definition."""
from abc import ABC, abstractmethod
from typing import Any, List

from AlteryxPythonSDK import RecordRef


class BaseRecordContainer(ABC):
    """Container for records."""

    __slots__ = ["records"]

    def __init__(self) -> None:
        """Construct a record container."""
        self.records: List[Any] = []

    @abstractmethod
    def add_record(self, record: RecordRef) -> None:
        """Make a copy of the record and add it to the container."""

    def clear_records(self) -> None:
        """Clear all accumulated records."""
        self.records = []
