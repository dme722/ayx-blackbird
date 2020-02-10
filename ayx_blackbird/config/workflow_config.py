"""Alteryx tool workflow configuration definition."""
from collections import UserDict
from copy import deepcopy

import xmltodict


class WorkflowConfiguration(UserDict):
    """Workflow configuration."""

    __slots__ = ["data", "original_data"]

    def __init__(self, config_str: str):
        """Initialize a workflow configuration."""
        self.data = xmltodict.parse(config_str, strip_whitespace=False)["Configuration"]
        self.original_data = deepcopy(self.data)
