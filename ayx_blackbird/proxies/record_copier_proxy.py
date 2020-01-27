"""RecordCopierProxy class definition."""
from typing import Mapping

from AlteryxPythonSDK import RecordCopier, RecordCreator, RecordInfo, RecordRef


class RecordCopierProxy:
    """Proxy for RecordCopier class from raw Python SDK."""

    __slots__ = ["_input_record_info", "_output_record_info", "_record_copier"]

    def __init__(
        self,
        input_record_info: RecordInfo,
        output_record_info: RecordInfo,
        field_name_map: Mapping[str, str],
    ):
        """Construct a record copier proxy object."""
        self._input_record_info = input_record_info
        self._output_record_info = output_record_info
        self._record_copier = RecordCopier(input_record_info, output_record_info)

        for input_name, output_name in field_name_map.items():
            input_idx = input_record_info.get_field_num(input_name)
            storage_idx = output_record_info.get_field_num(output_name)

            self._record_copier.add(storage_idx, input_idx)

        self._record_copier.done_adding()

    def copy(self, record: RecordRef) -> RecordCreator:
        """Copy a record into a new record creator."""
        record_creator = self._output_record_info.construct_record_creator()
        self._record_copier.copy(record_creator, record)

        return record_creator
