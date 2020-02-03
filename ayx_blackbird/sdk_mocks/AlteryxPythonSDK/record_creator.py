"""Mock record creator class definition."""
from .record_ref import RecordRef


class RecordCreator:
    """Record Creator mock."""

    def finalize_record(self) -> RecordRef:
        pass

    def reset(self, var_data_size: int = 0) -> None:
        pass
