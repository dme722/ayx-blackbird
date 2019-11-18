import AlteryxPythonSDK as sdk


class RecordContainer:
    def __init__(self, record_info, records=None):
        self._record_info = record_info

        self._record_copier = sdk.RecordCopier(record_info, record_info)

        for index in range(record_info.num_fields):
            self._record_copier.add(index, index)

        self._record_copier.done_adding()

        self._record_creator = self._record_info.construct_record_creator()

        if records is None:
            self.record_list = []
        else:
            self.record_list = list(records)

        self._fields = {field.name: FieldProxy(field)for field in record_info}

    def add_record(self, record, copy=True) -> None:
        if copy:
            self._record_copier.copy(self._record_creator, record)
            record = self._record_creator.finalize_record()
            self._record_creator.reset()

        self.record_list.append(record)

    def set_records(self, other) -> None:
        self.record_list = other

    def clear_records(self) -> None:
        self.record_list = []

    def set_from_df(self, df):
        if set(list(df)) != set(self._fields.keys()):
            raise ValueError("Dataframe must contain same columns as record container fields.")

        self.clear_records()
        for column_name in list(df):
            for _, value in df[column_name].items():
                field = self._fields[column_name]
                field.set(self._record_creator, value)

        self.add_record(self._record_creator.finalize_record(), copy=False)

    def parse_to_df(self, field_names=None):
        import pandas as pd

        if field_names is None:
            fields = self._fields
        else:
            fields = [self._fields[field_name] for field_name in field_names]

        return pd.DataFrame(
            {
                field.name: [field.get(record) for record in self]
                for field in fields
            }
        )

    def __iter__(self):
        yield from self.record_list

    def __len__(self):
        return len(self.record_list)


class FieldProxy:
    field_getters_map = {
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
        "spatialobj": "get_as_blob",
    }

    field_setters_map = {
        "bool": "set_from_bool",
        "blob": "set_from_blob",
        "double": "set_from_double",
        "float": "set_from_double",
        "fixeddecimal": "set_from_double",
        "byte": "set_from_int32",
        "int16": "set_from_int32",
        "int32": "set_from_int32",
        "int64": "set_from_int64",
        "string": "set_from_string",
        "v_string": "set_from_string",
        "v_wstring": "set_from_string",
        "wstring": "set_from_string",
        "date": "set_from_string",
        "datetime": "set_from_string",
        "time": "set_from_string",
    }

    field_cast_map = {
        "bool": bool,
        "blob": bytes,
        "double": float,
        "float": float,
        "fixeddecimal": float,
        "byte": int,
        "int16": int,
        "int32": int,
        "int64": int,
        "string": str,
        "v_string": str,
        "v_wstring": str,
        "wstring": str,
        "date": str,
        "datetime": str,
        "time": str,
    }

    def __init__(self, raw_field):
        self._raw_field = raw_field

        field_type = str(raw_field.type)
        self._getter = getattr(raw_field, self.field_getters_map[field_type])
        self._setter = getattr(raw_field, self.field_setters_map[field_type])
        self._caster = self.field_cast_map[field_type]

    def get(self, record):
        return self._caster(self._getter(record))

    def set(self, record_creator, value):
        import numpy as np

        if value is None:
            return self.set_null(record_creator)

        try:
            if not np.isfinite(value):
                return self.set_null(record_creator)
        except TypeError:
            pass

        return self._setter(record_creator, self._caster(value))

    def __getattr__(self, item):
        return getattr(self._raw_field, item)
