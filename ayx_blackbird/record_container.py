"""Record container definition."""
import AlteryxPythonSDK as sdk

from .constants import NULL_VALUE_PLACEHOLDER
from .field_proxy import FieldProxy
from .record_proxy import RecordProxy


class RecordContainer:
    __slots__ = ["__record_info", "_record_copier", "_records", "_fields"]

    def __init__(self, record_info):
        self.__record_info = record_info

        self._record_copier = sdk.RecordCopier(record_info, record_info)

        for index in range(record_info.num_fields):
            self._record_copier.add(index, index)

        self._record_copier.done_adding()

        self._records = []

        self._fields = {field.name: FieldProxy(field) for field in record_info}

    @property
    def record_info(self):
        return self.__record_info

    def add_record(self, record, copy=True) -> None:
        if copy:
            record_creator = self.get_record_creator()
            self._record_copier.copy(record_creator, record)
            record_proxy = RecordProxy(record_creator=record_creator)
        else:
            record_proxy = RecordProxy(record_ref=record)

        self.add_record_from_proxy(record_proxy)

    def add_record_from_proxy(self, record_proxy):
        self._records.append(record_proxy)

    def get_record_creator(self):
        return self.record_info.construct_record_creator()

    def set_records(self, other) -> None:
        self._records = other._records[:]

    def clear_records(self) -> None:
        self._records = []

    def set_from_df(self, df):
        if set(list(df)) != set(self._fields.keys()):
            raise ValueError(
                "Dataframe must contain same columns as record container fields."
            )

        self.fill_df_nulls_with_blackbird_nulls(df)

        fields = [self._fields[column_name] for column_name in list(df)]

        num_rows, _ = df.shape
        df_data = df.values

        self.clear_records()
        for row_index in range(num_rows):
            row = df_data[row_index]
            self._records.append(self._create_record_from_df_row(fields, row))

    def _create_record_from_df_row(self, fields, row):
        record_creator = self.get_record_creator()
        for col_index, field in enumerate(fields):
            field.set(record_creator, row[col_index])

        return RecordProxy(record_creator=record_creator)

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

    @staticmethod
    def fill_df_nulls_with_blackbird_nulls(df):
        df.fillna(NULL_VALUE_PLACEHOLDER, inplace=True)

    def __iter__(self):
        yield from self._records

    def __len__(self):
        return len(self._records)
