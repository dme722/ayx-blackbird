"""Alteryx plugin input anchor definition."""


class InputAnchor:
    """Input anchor to the tool"""

    def __init__(self, name: str, optional: bool):
        """Instantiate an input anchor."""
        self.name = name
        self.optional = optional
        self.connections = []
