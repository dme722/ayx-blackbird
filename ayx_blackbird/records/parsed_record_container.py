"""ParsedRecordContainer class definition."""
from typing import Any, List, Optional, TYPE_CHECKING

from AlteryxPythonSDK import RecordInfo, RecordRef

from .base_record_container import BaseRecordContainer
from ..proxies import FieldProxy

if TYPE_CHECKING:
    import pandas as pd


class ParsedRecordContainer(BaseRecordContainer):
    """Container for parsing and holding parsed records."""

    __slots__ = ["records", "_input_fields", "_field_names_to_parse", "_parse_fields"]

    def __init__(
        self,
        input_record_info: RecordInfo,
        field_names_to_parse: Optional[List[str]] = None,
    ) -> None:
        """Construct a container."""
        self._input_fields = {
            field.name: FieldProxy(field) for field in input_record_info
        }

        if field_names_to_parse is None:
            self._field_names_to_parse = [field.name for field in input_record_info]
        else:
            self._field_names_to_parse = field_names_to_parse

        self._parse_fields = [
            self._input_fields[field_name] for field_name in self._field_names_to_parse
        ]

        self.records: List[List[Any]] = []

    def add_record(self, record: RecordRef) -> None:
        """Add a new record to the container and parse it."""
        self.records.append(self._parse_record(record))

    def _parse_record(self, record: RecordRef) -> List[Any]:
        return [field.get(record) for field in self._parse_fields]

    def build_dataframe(self) -> "pd.DataFrame":
        """Build a dataframe out of the parsed records."""
        import pandas as pd

        return pd.DataFrame(self.records, columns=self._field_names_to_parse)
