from types import Optional

from .record_container import RecordContainer


class OutputAnchor:
    def __init__(
        self,
        name: str,
        optional: bool,
        engine_output_anchor_mgr,
        record_info=None,
        record_container: Optional[RecordContainer] = None,
    ):
        self.name = name
        self.optional = optional
        self.num_connections = 0
        self.record_info = record_info
        self.record_container = record_container

        self._engine_anchor_ref = engine_output_anchor_mgr.get_output_anchor(name)
        self._metadata_pushed = False

    def update_progress(self, percent: float) -> None:
        self._engine_anchor_ref.update_progress(percent)

    def push_metadata(self) -> None:
        if self.record_info is None:
            raise ValueError("record_info must be set before metadata can be pushed.")

        if not self._metadata_pushed:
            self._engine_anchor_ref.init(self.record_info)
            self._metadata_pushed = True

    def push_records(self) -> None:
        if not self._metadata_pushed:
            raise RuntimeError("Must run push_metadata before push_records can be called.")

        for record in self.record_container:
            self._engine_anchor_ref.push_record(record, False)

    def close(self) -> None:
        self._engine_anchor_ref.close()
