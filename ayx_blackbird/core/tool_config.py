"""Alteryx tool configuration definition."""
import os
from pathlib import Path
from typing import List, Mapping

import xmltodict

from ..anchors import InputAnchor, OutputAnchor


class ToolConfiguration:
    """Tool configuration definition."""

    __slots__ = ["tool_name", "_tool_config", "_output_anchor_mgr"]

    def __init__(self, tool_name: str, output_anchor_mgr):
        """Initialize a tool configuration."""
        self.tool_name = tool_name
        self._tool_config = self._get_tool_config()
        self._output_anchor_mgr = output_anchor_mgr

    def _get_tool_config(self) -> Mapping:
        with open(self._get_tool_config_filepath()) as fd:
            tool_config = xmltodict.parse(fd.read())

        return tool_config

    def _get_tool_config_filepath(self) -> Path:
        return Path(os.path.join(self._get_tool_path(), f"{self.tool_name}Config.xml"))

    def _get_tool_path(self) -> Path:
        return Path(os.path.join(self._get_tools_location(), self.tool_name))

    @staticmethod
    def _get_tools_location() -> Path:
        # TODO: Determine if user or admin
        # admin_path = os.path.join(os.environ["ALLUSERSPROFILE"], "Alteryx", "Tools")
        user_path = os.path.join(os.environ["APPDATA"], "Alteryx", "Tools")

        return Path(user_path)

    def build_input_anchors(self) -> List[InputAnchor]:
        """Build the input anchors based on tool config settings."""
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        input_anchor_configs = anchor_settings["InputConnections"]["Connection"]
        if not isinstance(input_anchor_configs, list):
            input_anchor_configs = [input_anchor_configs]

        return [
            InputAnchor(config["@Name"], config["@Optional"].lower() == "True")
            for config in input_anchor_configs
        ]

    def build_output_anchors(self) -> List[OutputAnchor]:
        """Build the output anchors based on tool config settings."""
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        output_anchor_configs = anchor_settings["OutputConnections"]["Connection"]
        if not isinstance(output_anchor_configs, list):
            output_anchor_configs = [output_anchor_configs]

            return [
                OutputAnchor(
                    config["@Name"],
                    config["@Optional"].lower() == "True",
                    self._output_anchor_mgr,
                )
                for config in output_anchor_configs
            ]
