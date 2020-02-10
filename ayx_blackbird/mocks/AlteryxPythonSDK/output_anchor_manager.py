"""Mock output anchor manager class definition."""
from typing import Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from .output_anchor import OutputAnchor


class OutputAnchorManager:
    """Output anchor manager mock."""

    def __init__(self, output_anchor_map: Mapping[str, "OutputAnchor"]):
        self._output_anchor_map = output_anchor_map

    def get_output_anchor(self, output_connection_name: str) -> "OutputAnchor":
        """Get an output anchor by name."""
        return self._output_anchor_map[output_connection_name]
