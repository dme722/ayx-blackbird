"""Mock record copier class definition."""
from .record_creator import RecordCreator
from .record_info import RecordInfo
from .record_ref import RecordRef


class RecordCopier:
    """Record copier mock."""

    def __init__(
        self,
        destination: RecordInfo,
        source: RecordInfo,
        suppress_size_only_conversion_errors: bool = False,
        decimal_separator: str = ".",
    ) -> None:
        self.destination = destination
        self.source = source
        self.supress_size_only_conversion_errors = suppress_size_only_conversion_errors
        self.decimal_separator = decimal_separator

    def add(self, destination_field_num: int, source_field_num: int) -> None:
        pass

    def done_adding(self) -> None:
        pass

    def copy(self, destination: RecordCreator, source: RecordRef) -> None:
        pass

    def set_dest_to_null(self, destination: RecordCreator) -> None:
        pass
