from typing import Any, List, Optional

from ..proxies import FieldProxy, RecordProxy


class ParsedRecordContainer:
    def __init__(
        self, input_record_info, field_names_to_parse: Optional[List[str]] = None
    ):
        self._input_fields = {
            field.name: FieldProxy(field) for field in input_record_info
        }

        self._field_names_to_parse = field_names_to_parse
        if field_names_to_parse is None:
            self._field_names_to_parse = [field.name for field in input_record_info]

        self.records = []

    def add_record(self, record: RecordProxy) -> None:
        self.records.append(self._parse_record(record))

    def _parse_record(self, record: RecordProxy) -> List[Any]:
        return [
            self._input_fields[field_name].get(record)
            for field_name in self._field_names_to_parse
        ]

    def clear_records(self) -> None:
        self.records = []

    @property
    def dataframe(self):
        import pandas as pd

        return pd.DataFrame(self.records, columns=list(self._input_fields.keys()))
