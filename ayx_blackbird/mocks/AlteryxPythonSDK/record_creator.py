"""Mock record creator class definition."""
from .record_ref import RecordRef


class RecordCreator:
    """Record Creator mock."""

    def __init__(self) -> None:
        """Construct a record creator."""
        self.record_ref = RecordRef()

    def finalize_record(self) -> RecordRef:
        """Finalize a record ref."""
        return self.record_ref

    def reset(self, var_data_size: int = 0) -> None:
        """Reset the creator."""
        self.record_ref = RecordRef()

    def set_field(self, name: str, value: Any) -> None:
        """Set a field in the underlying record ref."""
        self.record_ref.set_field(name, value)
