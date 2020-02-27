"""Alteryx Engine Proxy definition."""
from typing import Iterable

import AlteryxPythonSDK as Sdk

import xmltodict

from ..config import WorkflowConfiguration


class EngineProxy:
    """Proxy for the engine with a simplified interface."""

    __slots__ = ["engine", "tool_id"]

    def __init__(self, engine: Sdk.AlteryxEngine, tool_id: int):
        self.engine = engine
        self.tool_id = tool_id

    def xmsg(self, message: str, *args: Iterable[str]) -> str:
        """Localize a string."""
        return self.engine.xmsg(message, *args)

    def error(self, message: str) -> None:
        """Display an error message in the results panel."""
        self.engine.output_message(
            self.tool_id, Sdk.EngineMessageType.error, str(message)
        )

    def warning(self, message: str) -> None:
        """Display a warning message in the results panel."""
        self.engine.output_message(
            self.tool_id, Sdk.EngineMessageType.warning, str(message)
        )

    def info(self, message: str) -> None:
        """Display an info message in the results panel."""
        self.engine.output_message(
            self.tool_id, Sdk.EngineMessageType.info, str(message)
        )

    @property
    def update_only_mode(self) -> bool:
        """Check if the engine is running in update only mode."""
        return bool(self.engine.get_init_var(self.tool_id, "UpdateOnly") == "True")

    @property
    def designer_version(self) -> str:
        return self.engine.get_init_var(self.tool_id, "Version")

    def update_config_xml(self, workflow_config: WorkflowConfiguration) -> None:
        """Update the config XML of this tool if it has changed."""
        if workflow_config.original_data != workflow_config.data:
            self.engine.output_message(
                self.tool_id,
                Sdk.Status.update_output_config_xml,
                xmltodict.unparse({"Configuration": workflow_config.data}),
            )

    def output_tool_progress(self, percent: float) -> None:
        """Update tool progress."""
        self.engine.output_tool_progress(self.tool_id, percent)

    def create_record_info(self) -> Sdk.RecordInfo:
        """Create a new empty record info object."""
        return Sdk.RecordInfo(self.engine)

    def create_temp_file(self, extension: str = "tmp", options: int = 0) -> str:
        """Create a temporary file managed by Designer."""
        return self.engine.create_temp_file_name(extension, options)
