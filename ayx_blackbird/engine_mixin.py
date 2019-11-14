import AlteryxPythonSDK as sdk

import xmltodict

from .workflow_config import WorkflowConfiguration

class EngineProxy:
    def __init__(self, engine, tool_id):
        self._engine = engine
        self._tool_id = tool_id

    def xmsg(self, message: str) -> str:
        return message

    def error(self, message: str) -> None:
        self._engine.output_message(self._tool_id, sdk.EngineMessageType.error, message)

    def warning(self, message: str) -> None:
        self._engine.output_message(self._tool_id, sdk.EngineMessageType.warning, message)

    def info(self, message: str) -> None:
        self._engine.output_message(self._tool_id, sdk.EngineMessageType.info, message)

    @property
    def update_only_mode(self) -> bool:
        return self._engine.get_init_var(self._tool_id, "UpdateOnly") == "True"

    def update_config_xml(self, workflow_config: WorkflowConfiguration):
        if workflow_config.original_data != workflow_config.data:
            self._engine.output_message(self._tool_id, sdk.Status.update_output_config_xml, xmltodict.unparse({"Configuration": workflow_config.data}))