"""Mock alteryx engine class definition."""
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable

from .constants import EngineMessageType, Status
from .tool_execution_info import ToolExecutionInfo


class AlteryxEngine:
    """Alteryx Engine mock."""

    def __init__(self) -> None:
        """Construct an engine."""
        self.init_vars: Dict[str, str] = {
            "ActionApplies": "False",
            "AllowDesktopInteraction": "False",
            "DefaultDir": ".",
            "EnablePerformanceProfiling": "False",
            "NumThreads": "1",
            "OutputRecordCounts": "False",
            "RunMode": "Standard",
            "RunningAsWizard": "False",
            "RuntimeDataPath": ".",
            "SerialNumber": "MockSerial#123",
            "SettingsPath": ".",
            "TempPath": "./temp_dir/",
            "UpdateMode": "",
            "UpdateOnly": "False",
            "Version": "2020.1",
        }

        self.tool_execution_info: DefaultDict[int, ToolExecutionInfo] = defaultdict(
            ToolExecutionInfo
        )

    @staticmethod
    def create_temp_file_name(extension: str = "tmp", options: int = 0) -> str:
        """Create temp file."""
        import tempfile

        return tempfile.NamedTemporaryFile(suffix="." + extension).name

    def decrypt_password(self, encrypted_password: str, mode: int) -> str:
        """Decrypt password."""
        raise NotImplementedError()

    def get_constant(self, tool_id: int, which: int) -> None:
        """Get constant."""
        raise NotImplementedError()

    def get_init_var(self, tool_id: int, var_name: str) -> str:
        """Get initialization variable."""
        return self.init_vars[var_name]

    def output_message(self, tool_id: int, status: int, message: str) -> int:
        """Output message."""
        execution_info = self.tool_execution_info[tool_id]

        {
            EngineMessageType.error: execution_info.add_error,
            EngineMessageType.warning: execution_info.add_warning,
            EngineMessageType.info: execution_info.add_info,
            Status.update_output_config_xml: execution_info.set_output_workflow_xml,
        }[status](message)

        return 0

    def output_tool_progress(self, tool_id: int, percent_progress: float) -> None:
        """Output tool progress."""
        self.tool_execution_info[tool_id].progress = percent_progress

    def pre_sort(
        self,
        incoming_connection_type: str,
        incoming_connection_name: str,
        sort_info: str,
    ) -> None:
        """Presort records."""
        raise NotImplementedError()

    def xmsg(self, msg: str, *args: Iterable[str]) -> str:
        return msg
