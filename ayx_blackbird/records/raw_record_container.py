from typing import Mapping

from ..proxies import FieldProxy, RecordCopierProxy, RecordProxy
from ..utilities import fill_df_nulls_with_blackbird_nulls


class RawRecordContainer:
    __slots__ = [
        "records",
        "_input_record_info",
        "_storage_record_info",
        "_field_map",
        "_record_copier",
        "_input_fields",
    ]

    def __init__(
        self,
        input_record_info=None,
        storage_record_info=None,
        field_map: Mapping[str, str] = None,
    ):
        self._input_record_info = input_record_info
        self._storage_record_info = storage_record_info
        self._field_map = field_map
        self._record_copier = RecordCopierProxy(
            self._input_record_info, self._storage_record_info, self._field_map
        )
        self._input_fields = {
            field.name: FieldProxy(field) for field in input_record_info
        }
        self.records = []

    def add_record(self, record: RecordProxy) -> None:
        self.records.append(self._record_copier.copy(record))

    def clear_records(self) -> None:
        self.records = []

    def update_with_dataframe(self, df):
        num_rows, _ = df.shape

        if num_rows != len(self.records):
            raise ValueError(
                "Dataframe and source container must have the same number of records."
            )

        fill_df_nulls_with_blackbird_nulls(df)

        for record, (_, row) in zip(self.records, df.iterrows()):
            for column_name in list(df):
                field = self._storage_record_info.get_field_by_name(column_name)
                field.set(record, row[column_name])
