"""Mock field class definition."""
from .constants import FieldType
from .record_creator import RecordCreator
from .record_ref import RecordRef


class Field:
    """Field mock."""

    def __init__(
        self,
        name: str,
        type: FieldType,
        size: int,
        scale: int,
        source: str,
        description: str,
    ) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.scale = scale
        self.source = source
        self.description = description

    def equal_type(self, other_field: Field) -> bool:
        return (
            self.type == other_field.type
            and self.size == other_field.size
            and self.scale == other_field.scale
        )

    def get_as_bool(self, record_ref: RecordRef) -> bool:
        pass

    def get_as_double(self, record_ref: RecordRef) -> float:
        pass

    def get_as_int32(self, record_ref: RecordRef) -> int:
        pass

    def get_as_int64(self, record_ref: RecordRef) -> int:
        pass

    def get_as_string(self, record_ref: RecordRef) -> str:
        pass

    def get_as_blob(self, record_ref: RecordRef) -> bytes:
        pass

    def get_null(self, record_ref: RecordRef) -> bool:
        pass

    def set_from_bool(self, record_creator: RecordCreator, value: bool) -> None:
        pass

    def set_from_double(self, record_creator: RecordCreator, value: float) -> None:
        pass

    def set_from_int32(self, record_creator: RecordCreator, value: int) -> None:
        pass

    def set_from_int64(self, record_creator: RecordCreator, value: int) -> None:
        pass

    def set_from_string(self, record_creator: RecordCreator, value: str) -> None:
        pass

    def set_from_blob(self, record_creator: RecordCreator, value: bytes) -> None:
        pass

    def set_null(self, record_creator: RecordCreator) -> None:
        pass
