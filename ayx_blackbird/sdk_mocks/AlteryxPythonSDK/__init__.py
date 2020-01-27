"""Mocks for testing."""
from .alteryx_engine import AlteryxEngine
from .field import Field
from .output_anchor import OutputAnchor
from .output_anchor_manager import OutputAnchorManager
from .record_copier import RecordCopier
from .record_creator import RecordCreator
from .record_info import RecordInfo
from .record_ref import RecordRef

__all__ = [
    "AlteryxEngine",
    "Field",
    "RecordInfo",
    "RecordCopier",
    "RecordCreator",
    "RecordRef",
    "OutputAnchor",
    "OutputAnchorManager",
]
