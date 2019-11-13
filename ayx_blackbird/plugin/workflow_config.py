from copy import deepcopy

import xmltodict


class WorkflowConfiguration:
    def __init__(self, config_str, engine):
        self.config = xmltodict.parse(config_str)["Configuration"]
        self._original_config = deepcopy(self.config)
