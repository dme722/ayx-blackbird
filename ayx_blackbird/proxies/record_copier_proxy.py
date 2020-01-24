import AlteryxPythonSDK as Sdk

from .record_proxy import RecordProxy


class RecordCopierProxy:
    def __init__(self, input_record_info, output_record_info, field_name_map):
        self._input_record_info = input_record_info
        self._output_record_info = output_record_info
        self._record_copier = Sdk.RecordCopier(input_record_info, output_record_info)

        for input_name, output_name in field_name_map.items():
            input_idx = input_record_info.get_field_num(input_name)
            storage_idx = output_record_info.get_field_num(output_name)

            self._record_copier.add(storage_idx, input_idx)

        self._record_copier.done_adding()

    def copy(self, record):
        record_creator = self._output_record_info.construct_record_creator()
        self._record_copier.copy(record_creator, record.value)

        return RecordProxy(record_creator=record_creator)
