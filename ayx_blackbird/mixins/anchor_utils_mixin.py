"""AnchorUtilsMixin class definition."""
from typing import List

from ..anchors import InputAnchor, OutputAnchor
from ..utilities.constants import ConnectionStatus
from ..utilities.exceptions import AnchorNotFoundException


class AnchorUtilsMixin:
    """Utility functions for interacting with input and output anchors."""

    def __init__(self) -> None:
        self.input_anchors: List[InputAnchor] = []
        self.output_anchors: List[OutputAnchor] = []

    def push_all_metadata(self) -> None:
        """Push all metadata for anchors."""
        for anchor in self.output_anchors:
            anchor.push_metadata()

    def close_output_anchors(self) -> None:
        """Close connection for all output anchors."""
        for anchor in self.output_anchors:
            anchor.close()

    def get_input_anchor(self, input_anchor_name: str) -> InputAnchor:
        """Get an input anchor by name."""
        try:
            return [
                anchor
                for anchor in self.input_anchors
                if anchor.name == input_anchor_name
            ][0]
        except IndexError:
            raise AnchorNotFoundException(f"{input_anchor_name} not found.")

    def get_output_anchor(self, output_anchor_name: str) -> OutputAnchor:
        """Get an output anchor by name."""
        try:
            return [
                anchor
                for anchor in self.output_anchors
                if anchor.name == output_anchor_name
            ][0]
        except IndexError:
            raise AnchorNotFoundException(f"{output_anchor_name} not found.")

    @property
    def all_required_connections_connected(self) -> bool:
        """Getter for if all required connections are connected."""
        return all(
            [len(anchor.connections) > 0 for anchor in self.required_input_anchors]
        )

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
