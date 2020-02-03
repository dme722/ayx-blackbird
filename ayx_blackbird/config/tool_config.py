"""Alteryx tool configuration definition."""
import os
from pathlib import Path
from typing import Any, Dict, List

from AlteryxPythonSDK import OutputAnchorManager

import xmltodict

from ..anchors import InputAnchor, OutputAnchor


class ToolConfiguration:
    """Tool configuration definition."""

    __slots__ = ["tool_name", "_tool_config", "_output_anchor_mgr"]

    def __init__(self, tool_name: str, output_anchor_mgr: OutputAnchorManager):
        """Initialize a tool configuration."""
        self.tool_name = tool_name
        self._tool_config = self._get_tool_config()
        self._output_anchor_mgr = output_anchor_mgr

    def _get_tool_config(self) -> Dict[str, Any]:
        with open(str(self._get_tool_config_filepath())) as fd:
            tool_config = dict(xmltodict.parse(fd.read()))

        return tool_config

    def _get_tool_config_filepath(self) -> Path:
        return Path(
            os.path.join(str(self._get_tool_path()), f"{self.tool_name}Config.xml")
        )

    def _get_tool_path(self) -> Path:
        return Path(os.path.join(str(self._get_tools_location()), self.tool_name))

    @staticmethod
    def _get_tools_location() -> Path:
        # TODO: Determine if user or admin
        # admin_path = os.path.join(os.environ["ALLUSERSPROFILE"], "Alteryx", "Tools")
        user_path = os.path.join(os.environ["APPDATA"], "Alteryx", "Tools")

        return Path(user_path)

    def build_input_anchors(self) -> List[InputAnchor]:
        """Build the input anchors based on tool config settings."""
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        input_anchors = anchor_settings.get("InputConnections")
        if input_anchors is None:
            input_anchor_configs = []
        else:
            input_anchor_configs_raw = input_anchors["Connection"]
            if not isinstance(input_anchor_configs_raw, list):
                input_anchor_configs = [input_anchor_configs_raw]
            else:
                input_anchor_configs = input_anchor_configs_raw

        return [
            InputAnchor(config["@Name"], config["@Optional"].lower() == "True")
            for config in input_anchor_configs
        ]

    def build_output_anchors(self) -> List[OutputAnchor]:
        """Build the output anchors based on tool config settings."""
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        output_anchors = anchor_settings.get("OutputConnections")

        if output_anchors is None:
            output_anchor_configs = []
        else:
            output_anchor_configs_raw = output_anchors["Connection"]
            if not isinstance(output_anchor_configs_raw, list):
                output_anchor_configs = [output_anchor_configs_raw]
            else:
                output_anchor_configs = output_anchor_configs_raw

        return [
            OutputAnchor(
                config["@Name"],
                config["@Optional"].lower() == "True",
                self._output_anchor_mgr,
            )
            for config in output_anchor_configs
        ]
