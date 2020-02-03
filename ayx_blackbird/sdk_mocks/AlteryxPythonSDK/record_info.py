"""Mock record info class definition."""
from typing import Generator, List, Optional

from .alteryx_engine import AlteryxEngine
from .constants import FieldType
from .field import Field
from .record_creator import RecordCreator


class RecordInfo:
    """Record info mock."""

    def __init__(self, alteryx_engine: AlteryxEngine) -> None:
        self._fields: List[Field] = []

    def add_field(
        self,
        field_name: str,
        field_type: FieldType,
        size: int = 0,
        scale: int = 0,
        source: str = "",
        description: str = "",
    ) -> Field:
        pass

    def add_field_from_xml(self, xml: str, name_prefix: str = "") -> Field:
        pass

    def clone(self) -> RecordInfo:
        pass

    def construct_record_creator(self) -> RecordCreator:
        pass

    def equal_types(
        self, record_info: RecordInfo, allow_additional_fields: bool = False
    ) -> bool:
        pass

    def get_field_by_name(
        self, field_name: str, throw_error: bool = True
    ) -> Optional[Field]:
        pass

    def get_field_num(self, field_name: str, throw_error: bool = True) -> int:
        pass

    def get_hash(self) -> int:
        pass

    def get_record_xml_meta_data(self, include_source: bool = True) -> str:
        pass

    def init_from_xml(self, xml: str, name_prefix: str = "") -> None:
        pass

    def rename_field_by_index(self, field_idx: int, new_name: str) -> Field:
        pass

    def rename_field_by_name(self, old_name: str, new_name: str) -> Field:
        pass

    def swap_field_names(self, field_1: int, field_2: int) -> None:
        pass

    def __iter__(self) -> Generator[Field, None, None]:
        yield from self._fields
