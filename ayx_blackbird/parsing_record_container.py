"""Parsing record container definition."""
from .record_container import RecordContainer


class ParsingRecordContainer(RecordContainer):
    def __init__(self, record_info):
        super().__init__(record_info)

        self._parsed_records = []

    def add_record(self, record, copy=True) -> None:
        if copy:
            record_creator = self.get_record_creator()
            self._record_copier.copy(record_creator, record)
            self._records.append(RecordProxy(record_creator=record_creator))
        else:
            self._records.append(RecordProxy(record_ref=record))

    def parse_to_df(self, field_names=None):
        import pandas as pd

        if field_names is None:
            fields = [field for _, field in self._fields.items()]
        else:
            fields = [self._fields[field_name] for field_name in field_names]

        return pd.DataFrame.from_records(
            [
                [
                    field.get(record.value)
                    for field in fields
                ]
                for record in self
            ],
            columns=[field.name for field in fields]
        )
