import AlteryxPythonSDK as sdk

class RecordContainer:
    def __init__(self, record_info):
        self._record_info = record_info

        self.record_copier = sdk.RecordCopier(record_info, record_info)

        for index in range(record_info.num_fields):
            self.record_copier.add(index, index)

        self.record_copier.done_adding()

        self._record_list = []

    def add_record(self, record):
        self._record_list.append(self._record_info.construct_record_creator())
        self.record_copier(self._record_list[-1], record)

type_dict = {
    "blob": "get_as_blob",
    "byte": "get_as_int32",
    "int16": "get_as_int32",
    "int32": "get_as_int32",
    "int64": "get_as_int64",
    "float": "get_as_double",
    "double": "get_as_double",
    "date": "get_as_string",
    "time": "get_as_string",
    "datetime": "get_as_string",
    "bool": "get_as_bool",
    "string": "get_as_string",
    "v_string": "get_as_string",
    "v_wstring": "get_as_string",
    "wstring": "get_as_string",
    "fixeddecimal": "get_as_double",
    "spatialobj": "get_as_blob"
}


def get_getter_from_field(field):
    return getattr(field, type_dict[str(field.type)])