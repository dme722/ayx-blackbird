"""Alteryx plugin input anchor definition."""
from typing import List


class InputAnchor:
    """Input anchor to the tool."""

    __slots__ = ["name", "optional", "connections"]

    def __init__(self, name: str, optional: bool):
        """Instantiate an input anchor."""
        from ..core.connection_interface import ConnectionInterface

        self.name = name
        self.optional = optional
        self.connections: List[ConnectionInterface] = []
