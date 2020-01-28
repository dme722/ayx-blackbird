"""FieldProxy class definition."""
from typing import Any

from AlteryxPythonSDK import Field, RecordCreator, RecordRef

from ..utilities.constants import NULL_VALUE_PLACEHOLDER


class FieldProxy:
    """Proxy for Field class from the raw Python SDK."""

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

    __slots__ = ["name", "_raw_field", "_getter", "_setter", "_caster", "_set_null"]

    def __init__(self, raw_field: Field):
        """Construct a field proxy object."""
        self.name = raw_field.name
        self._raw_field = raw_field

        field_type = str(raw_field.type)
        self._getter = getattr(raw_field, self.field_getters_map[field_type])
        self._setter = getattr(raw_field, self.field_setters_map[field_type])
        self._caster = self.field_cast_map[field_type]
        self._set_null = self._raw_field.set_null

    def get(self, record: RecordRef) -> Any:
        """Get the value for this field from a record."""
        return self._getter(record)

    def set(self, record_creator: RecordCreator, value: Any) -> None:
        """Set the field for a given record to a value."""
        if value is NULL_VALUE_PLACEHOLDER:
            return self.set_null(record_creator)

        self._setter(record_creator, self._caster(value))

    def set_null(self, record_creator: RecordCreator) -> None:
        """Set the field for a given record to null."""
        self._set_null(record_creator)
