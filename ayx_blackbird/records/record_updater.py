"""Record updater definition."""
import AlteryxPythonSDK as sdk

from .record_container import RecordContainer
from ..proxies import FieldProxy


class RecordUpdater:
    __slots__ = ["_src", "_dest", "_dest_fields", "_record_copier"]

    def __init__(self, src_container: RecordContainer, dest_container: RecordContainer):
        self._src = src_container
        self._dest = dest_container

        self._dest_fields = {field.name: FieldProxy(field) for field in self._dest.record_info}

        self._record_copier = sdk.RecordCopier(self._src.record_info, self._dest.record_info)

        for index, field in enumerate(self._src.record_info):
            self._record_copier.add(index, self._get_field_index(self._dest.record_info, field.name))

        self._record_copier.done_adding()

    @staticmethod
    def _get_field_index(record_info, field_name):
        for index, field in enumerate(record_info):
            if field.name == field_name:
                return index

        raise ValueError("Field not found.")

    def apply_update(self, df):
        num_rows, _ = df.shape

        if num_rows != len(self._src):
            raise ValueError("Dataframe and source container must have the same number of records.")

        self._dest.clear_records()

        RecordContainer.fill_df_nulls_with_blackbird_nulls(df)

        for record, (_, row) in zip(self._src, df.iterrows()):
            record_creator = self._dest.get_record_creator()
            self._record_copier.set_dest_to_null(record_creator)
            self._record_copier.copy(record_creator, record.finalize_record())

            for column_name in list(df):
                field = self._dest_fields[column_name]
                field.set(record_creator, row[column_name])

            self._dest.add_record_creator(record_creator)
