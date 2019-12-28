"""Alteryx Engine Proxy definition."""
import AlteryxPythonSDK as sdk

import xmltodict


class EngineProxy:
    """Proxy for the engine with a simplified interface."""
    __slots__ = ["_engine", "_tool_id"]

    def __init__(self, engine, tool_id):
        self._engine = engine
        self._tool_id = tool_id

    def xmsg(self, message: str) -> str:
        """Localize a string."""
        return message

    def error(self, message: str) -> None:
        """Display an error message in the results panel."""
        self._engine.output_message(self._tool_id, sdk.EngineMessageType.error, message)

    def warning(self, message: str) -> None:
        """Display a warning message in the results panel."""
        self._engine.output_message(
            self._tool_id, sdk.EngineMessageType.warning, message
        )

    def info(self, message: str) -> None:
        """Display an info message in the results panel."""
        self._engine.output_message(self._tool_id, sdk.EngineMessageType.info, message)

    @property
    def update_only_mode(self) -> bool:
        """Check if the engine is running in update only mode."""
        return self._engine.get_init_var(self._tool_id, "UpdateOnly") == "True"

    def update_config_xml(self, workflow_config):
        """Update the config XML of this tool if it has changed."""
        if workflow_config.original_data != workflow_config.data:
            self._engine.output_message(
                self._tool_id,
                sdk.Status.update_output_config_xml,
                xmltodict.unparse({"Configuration": workflow_config.data}),
            )

    def __getattr__(self, name):
        """Defer undefined methods to normal engine."""
        return getattr(self._engine, name)
