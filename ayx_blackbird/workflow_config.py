from collections import UserDict
from copy import deepcopy

import xmltodict


class WorkflowConfiguration(UserDict):
    def __init__(self, config_str: str):
        self.data = xmltodict.parse(config_str)["Configuration"]
        self.original_data = deepcopy(self.config)
