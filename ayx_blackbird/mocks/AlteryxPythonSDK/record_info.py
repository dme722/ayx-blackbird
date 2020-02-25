"""Mock record info class definition."""
from copy import deepcopy
from typing import Generator, List, Optional, TYPE_CHECKING

from .alteryx_engine import AlteryxEngine
from .constants import FieldType
from .record_creator import RecordCreator

from .field import Field


class RecordInfo:
    """Record info mock."""

    def __init__(self, alteryx_engine: AlteryxEngine) -> None:
        """Construct a record info."""
        self._fields: List["Field"] = []
        self.alteryx_engine = alteryx_engine

    def add_field(
        self,
        field_name: str,
        field_type: FieldType,
        size: int = 0,
        scale: int = 0,
        source: str = "",
        description: str = "",
    ) -> "Field":
        """Add a field to the record info."""
        self._fields.append(
            Field(
                name=field_name,
                type=field_type,
                size=size,
                scale=scale,
                source=source,
                description=description,
            )
        )

        return self._fields[-1]

    def add_field_from_xml(self, xml: str, name_prefix: str = "") -> "Field":
        """Add a field from an XML string definition."""
        raise NotImplementedError()

    def clone(self) -> "RecordInfo":
        """Make a copy of the record info."""
        return deepcopy(self)

    def construct_record_creator(self) -> RecordCreator:
        """Create a new record creator."""
        return RecordCreator(self)

    def equal_types(
        self, record_info: "RecordInfo", allow_additional_fields: bool = False
    ) -> bool:
        """Check if another record info object has equal types to this."""
        if not allow_additional_fields and len(self) < len(record_info):
            return False

        for self_field, other_field in zip(self, record_info):
            if self_field.type != other_field.type:
                return False

        return True

    def get_field_by_name(
        self, field_name: str, throw_error: bool = True
    ) -> Optional["Field"]:
        """Get a field object by field name."""
        for field in self:
            if field.name == field_name:
                return field

        if throw_error:
            raise RuntimeError("Field name not found.")

        return None

    def get_field_num(self, field_name: str, throw_error: bool = True) -> int:
        """Get the index of a field by name."""
        raise NotImplementedError()

    def get_hash(self) -> int:
        """Get hash of this record info."""
        raise NotImplementedError()

    def get_record_xml_meta_data(self, include_source: bool = True) -> str:
        """Get XML metadata string."""
        raise NotImplementedError()

    def init_from_xml(self, xml: str, name_prefix: str = "") -> None:
        """Initialize this record info from an XML string."""
        raise NotImplementedError()

    def rename_field_by_index(self, field_idx: int, new_name: str) -> "Field":
        """Rename a field by index."""
        raise NotImplementedError()

    def rename_field_by_name(self, old_name: str, new_name: str) -> "Field":
        """Rename a field by name."""
        raise NotImplementedError()

    def swap_field_names(self, field_1: int, field_2: int) -> None:
        """Swap two field names."""
        raise NotImplementedError()

    def __iter__(self) -> Generator["Field", None, None]:
        """Iterate over fields in this record info."""
        yield from self._fields

    def __len__(self) -> int:
        """Get the number of fields available."""
        return len(self._fields)
