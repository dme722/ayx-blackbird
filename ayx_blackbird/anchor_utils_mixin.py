"""AnchorUtilsMixin class definition."""
from typing import List

from .connection_interface import ConnectionStatus
from .input_anchor import InputAnchor


class AnchorUtilsMixin:
    """Utility functions for interacting with input and output anchors."""

    def push_all_records(self) -> None:
        """Push any records queued for output."""
        for anchor in self.output_anchors:
            anchor.push_records()

    def push_all_metadata(self) -> None:
        """Push all metadata for anchors."""
        for anchor in self.output_anchors:
            anchor.push_metadata()

    def close_output_anchors(self) -> None:
        """Close connection for all output anchors."""
        for anchor in self.output_anchors:
            anchor.close()

    def clear_all_input_records(self) -> None:
        """Remove all accumulated input records from input anchor record containers."""
        for anchor in self.input_anchors:
            for connection in anchor.connections:
                connection.record_container.clear_records()

    def get_input_anchor(self, input_anchor_name):
        """Get an input anchor by name."""
        return [
            anchor for anchor in self.input_anchors if anchor.name == input_anchor_name
        ][0]

    def get_output_anchor(self, output_anchor_name):
        """Get an output anchor by name"""
        return [
            anchor
            for anchor in self.output_anchors
            if anchor.name == output_anchor_name
        ][0]

    @property
    def all_connections_initialized(self) -> bool:
        """Getter for if all input connections are initialized."""
        return all(
            [
                connection.status != ConnectionStatus.CREATED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

    @property
    def all_connections_closed(self) -> bool:
        """Getter for if all input connections are closed."""
        return all(
            [
                connection.status == ConnectionStatus.CLOSED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

    @property
    def required_input_anchors(self) -> List[InputAnchor]:
        """Get the list of required input anchors for this tool."""
        return [anchor for anchor in self.input_anchors if not anchor.optional]
