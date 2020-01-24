"""Record container definition."""
import AlteryxPythonSDK as Sdk

from ..proxies import FieldProxy, RecordProxy


class RecordAccumulator:
    def __init__(self, raw_record_container=None, parsed_record_container=None):
        self.raw_record_container = raw_record_container
        self.parsed_record_container = parsed_record_container

    def add_record(self, record: RecordProxy) -> None:
        if self.raw_record_container:
            self.raw_record_container.add_record(record)

        if self.parsed_record_container:
            self.parsed_record_container.add_record(record)

    def clear_records(self):
        if self.raw_record_container:
            self.raw_record_container.clear_records()

        if self.parsed_record_container:
            self.parsed_record_container.clear_records()


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


class RawRecordContainer:
    def __init__(self, input_record_info=None, storage_record_info=None, field_map=None):
        self._input_record_info = input_record_info
        self._storage_record_info = storage_record_info
        self._field_map = field_map
        self.records = []
        self._record_copier = self.build_record_copier()
        self._input_fields = {field.name: FieldProxy(field) for field in input_record_info}

    def set_storage_record_info_and_field_map(self, record_info, field_map):
        self._storage_record_info = record_info
        self._field_map = field_map
        self._record_copier = self.build_record_copier()

    def build_record_copier(self):
        return RecordCopierProxy(self._input_record_info, self._storage_record_info, self._field_map)

    def add_record(self, record: RecordProxy):
        pass

    def clear_records(self):
        pass


class ParsedRecordContainer:
    def __init__(self, input_record_info, field_names_to_parse=None):
        self._input_fields = {field.name: FieldProxy(field) for field in input_record_info}
        self._field_names_to_parse = field_names_to_parse

    def add_record(self, record: RecordProxy):
        pass

    def _parse_record(self, record: RecordProxy):
        return [
            self._input_fields[field_name].get(record.value)
            for field_name in self._field_names_to_parse
        ]

    def clear_records(self):
        pass
