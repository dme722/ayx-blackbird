from typing import Any, List, Optional

from ..proxies import FieldProxy


class ParsedRecordContainer:
    __slots__ = ["records", "_input_fields", "_field_names_to_parse", "_parse_fields"]

    def __init__(
        self, input_record_info, field_names_to_parse: Optional[List[str]] = None
    ):
        self._input_fields = {
            field.name: FieldProxy(field) for field in input_record_info
        }

        self._field_names_to_parse = field_names_to_parse
        if field_names_to_parse is None:
            self._field_names_to_parse = [field.name for field in input_record_info]

        self._parse_fields = [
            self._input_fields[field_name] for field_name in self._field_names_to_parse
        ]

        self.records = []

    def add_record(self, record) -> None:
        self.records.append(self._parse_record(record))

    def _parse_record(self, record) -> List[Any]:
        return [field.get(record) for field in self._parse_fields]

    def clear_records(self) -> None:
        self.records = []

    def build_dataframe(self):
        import pandas as pd

        return pd.DataFrame(self.records, columns=self._field_names_to_parse)
