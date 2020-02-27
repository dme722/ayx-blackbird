"""Alteryx tool configuration definition."""
import os
from pathlib import Path
from typing import Any, Dict, List

from AlteryxPythonSDK import OutputAnchorManager

import xmltodict

from ..anchors import InputAnchor, OutputAnchor


class ToolConfiguration:
    """Tool configuration definition."""

    __slots__ = ["tool_name", "tool_config", "output_anchor_mgr"]

    def __init__(self, tool_name: str, output_anchor_mgr: OutputAnchorManager):
        """Initialize a tool configuration."""
        self.tool_name = tool_name
        self.tool_config = self.get_tool_config()
        self.output_anchor_mgr = output_anchor_mgr

    def get_tool_config(self) -> Dict[str, Any]:
        try:
            with open(str(self.get_tool_config_filepath())) as fd:
                tool_config = dict(xmltodict.parse(fd.read(), strip_whitespace=False))
        except FileNotFoundError:
            raise RuntimeError(f"Couldn't find tool with name {self.tool_name}.")
        else:
            return tool_config

    def get_tool_config_filepath(self) -> Path:
        """Get the path to the tool configuration file."""
        return Path(
            os.path.join(str(self.get_tool_path()), f"{self.tool_name}Config.xml")
        )

    def get_tool_path(self) -> Path:
        """Get the path to the directory containing the current tool's definition."""
        return Path(os.path.join(str(self.get_tools_location()), self.tool_name))

    def get_tools_location(self) -> Path:
        """Get the location of Alteryx tools that contain the current tool."""
        tools_rel_path = os.path.join("Alteryx", "Tools")
        admin_path = os.path.join(os.environ["ALLUSERSPROFILE"], tools_rel_path)
        user_path = os.path.join(os.environ["APPDATA"], tools_rel_path)

        if self.tool_name in os.listdir(user_path):
            return Path(user_path)

        return Path(admin_path)

    def build_input_anchors(self) -> List[InputAnchor]:
        """Build the input anchors based on tool config settings."""
        anchor_settings = self.tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

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
            InputAnchor(config["@Name"], config["@Optional"].lower() == "true")
            for config in input_anchor_configs
        ]

    def build_output_anchors(self) -> List[OutputAnchor]:
        """Build the output anchors based on tool config settings."""
        anchor_settings = self.tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

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
                config["@Optional"].lower() == "true",
                self.output_anchor_mgr,
            )
            for config in output_anchor_configs
        ]
