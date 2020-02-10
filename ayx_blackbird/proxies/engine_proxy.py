"""Alteryx Engine Proxy definition."""
import AlteryxPythonSDK as Sdk

import xmltodict

from ..config import WorkflowConfiguration


class EngineProxy:
    """Proxy for the engine with a simplified interface."""

    __slots__ = ["_engine", "_tool_id"]

    def __init__(self, engine: Sdk.AlteryxEngine, tool_id: int):
        self._engine = engine
        self._tool_id = tool_id

    def xmsg(self, message: str) -> str:
        """Localize a string."""
        return message

    def error(self, message: str) -> None:
        """Display an error message in the results panel."""
        self._engine.output_message(
            self._tool_id, Sdk.EngineMessageType.error, str(message)
        )

    def warning(self, message: str) -> None:
        """Display a warning message in the results panel."""
        self._engine.output_message(
            self._tool_id, Sdk.EngineMessageType.warning, str(message)
        )

    def info(self, message: str) -> None:
        """Display an info message in the results panel."""
        self._engine.output_message(
            self._tool_id, Sdk.EngineMessageType.info, str(message)
        )

    @property
    def update_only_mode(self) -> bool:
        """Check if the engine is running in update only mode."""
        return bool(self._engine.get_init_var(self._tool_id, "UpdateOnly") == "True")

    def update_config_xml(self, workflow_config: WorkflowConfiguration) -> None:
        """Update the config XML of this tool if it has changed."""
        if workflow_config.original_data != workflow_config.data:
            self._engine.output_message(
                self._tool_id,
                Sdk.Status.update_output_config_xml,
                xmltodict.unparse({"Configuration": workflow_config.data}),
            )

    def output_tool_progress(self, percent: float) -> None:
        """Update tool progress."""
        self._engine.output_tool_progress(self._tool_id, percent)

    def create_record_info(self) -> Sdk.RecordInfo:
        """Create a new empty record info object."""
        return Sdk.RecordInfo(self._engine)
