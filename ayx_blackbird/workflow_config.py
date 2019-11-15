"""Alteryx tool workflow configuration definition."""
from collections import UserDict
from copy import deepcopy

import xmltodict


class WorkflowConfiguration(UserDict):
    """Workflow configuration."""

    def __init__(self, config_str: str):
        """Initialize a workflow configuration."""
        self.data = xmltodict.parse(config_str)["Configuration"]
        self.original_data = deepcopy(self.config)
