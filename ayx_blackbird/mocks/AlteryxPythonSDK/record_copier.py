"""Mock record copier class definition."""
from typing import Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from .record_creator import RecordCreator
    from .record_info import RecordInfo
    from .record_ref import RecordRef


class RecordCopier:
    """Record copier mock."""

    def __init__(
        self,
        destination: "RecordInfo",
        source: "RecordInfo",
        suppress_size_only_conversion_errors: bool = False,
        decimal_separator: str = ".",
    ) -> None:
        """Construct a record copier."""
        self.destination = destination
        self.source = source
        self.supress_size_only_conversion_errors = suppress_size_only_conversion_errors
        self.decimal_separator = decimal_separator
        self._done_adding = False
        self._idx_map: Dict[int, int] = {}

    def add(self, destination_field_num: int, source_field_num: int) -> None:
        """Add a field to the record copier."""
        if self._done_adding:
            raise RuntimeError("Done adding, can't add any more.")

        self._idx_map[source_field_num] = destination_field_num

    def done_adding(self) -> None:
        """Signal that fields are done being added."""
        self._done_adding = True

    def copy(self, destination: "RecordCreator", source: "RecordRef") -> None:
        """Copy a record to the destination format."""
        for source_idx, dest_idx in self._idx_map.items():
            source_key = list(source.data.keys())[source_idx]
            dest_key = list(destination.record_ref.data.keys())[dest_idx]

            destination.record_ref.data[dest_key] = source.data[source_key]

    @staticmethod
    def set_dest_to_null(destination: "RecordCreator") -> None:
        """Set destination to all null."""
        for key in destination.record_ref.data:
            destination.record_ref.data[key] = None
