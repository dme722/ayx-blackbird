"""Alteryx plugin output anchor definition."""
from typing import Callable, Iterable, Optional

import AlteryxPythonSDK as Sdk


class OutputAnchor:
    """Output anchor definition."""

    __slots__ = [
        "_engine_anchor_ref",
        "_metadata_pushed",
        "__record_info",
        "name",
        "optional",
        "num_connections",
        "push_records",
    ]

    def __init__(
        self,
        name: str,
        optional: bool,
        output_anchor_mgr: Sdk.OutputAnchorManager,
        record_info: Optional[Sdk.RecordInfo] = None,
    ) -> None:
        """Initialize an output anchor."""
        engine_anchor_ref_optional = output_anchor_mgr.get_output_anchor(name)
        if engine_anchor_ref_optional is None:
            raise RuntimeError(f"Can't find output anchor: {name}")
        else:
            self._engine_anchor_ref: Sdk.OutputAnchor = engine_anchor_ref_optional

        self._metadata_pushed: bool = False
        self.__record_info = record_info
        self.name = name
        self.optional = optional
        self.num_connections: int = 0
        self.push_records: Callable = self._raise_metadata_error

    @property
    def record_info(self) -> Optional[Sdk.RecordInfo]:
        """Getter for record info."""
        return self.__record_info

    @record_info.setter
    def record_info(self, value: Sdk.RecordInfo) -> None:
        """Setter for record info."""
        if self._metadata_pushed:
            raise RuntimeError("Can't reassign record_info after it has been pushed.")

        self.__record_info = value

    def update_progress(self, percent: float) -> None:
        """Push the progress to downstream tools."""
        self._engine_anchor_ref.update_progress(percent)

    def push_metadata(self) -> None:
        """Push metadata to downstream tools."""
        if self.record_info is None:
            raise ValueError("record_info must be set before metadata can be pushed.")

        if not self._metadata_pushed:
            self._engine_anchor_ref.init(self.record_info)
            self._metadata_pushed = True
            self.push_records = self._push_records
        else:
            raise RuntimeError("Metadata is trying to be pushed a second time.")

    def _raise_metadata_error(self, _: Iterable[Sdk.RecordCreator]) -> None:
        """Push records out."""
        raise RuntimeError("Must run push_metadata before push_records can be called.")

    def _push_records(self, record_creators: Iterable[Sdk.RecordCreator]) -> None:
        """Push all records passed from iterable."""
        for record_creator in record_creators:
            self._engine_anchor_ref.push_record(record_creator.finalize_record(), False)

    def close(self) -> None:
        """Close the output anchor."""
        self._engine_anchor_ref.close()
