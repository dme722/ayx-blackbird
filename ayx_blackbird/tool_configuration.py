import os

from .input_anchor import InputAnchor
from .output_anchor import OutputAnchor

import xmltodict


class ToolConfiguration:
    def __init__(self, tool_name, output_anchor_mgr):
        self.tool_name = tool_name
        self._tool_config = self._get_tool_config()
        self._output_anchor_mgr = output_anchor_mgr

    def _get_tool_config(self):
        xml_files = [
            file
            for file in os.listdir(self._get_tool_path())
            if file.lower().endswith(".xml")
        ]

        if len(xml_files) > 0:
            raise RuntimeError("Multiple tool configuration XML files found. Only one can be present.")

        config_filepath = os.path.join(self._get_tool_path(), xml_files[0])

        with open(config_filepath) as fd:
            tool_config = xmltodict.parse(fd.read())

        return tool_config

    def _get_tool_path(self):
        return os.path.join(self._get_tools_location(), self.tool_name)

    @staticmethod
    def _get_tools_location():
        admin_path = os.path.join(os.environ["APPDATA"], "Alteryx", "Tools")
        user_path = os.path.join(os.environ["PROGRAMDATA"], "Alteryx", "Tools")
        if os.path.abspath(admin_path) in __file__:
            return admin_path

        if os.path.abspath(user_path) in __file__:
            return user_path

        raise RuntimeError("Tool is not located in Alteryx install locations.")

    def build_input_anchors(self):
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        input_anchor_configs = anchor_settings["InputConnections"]["Connection"]
        if not isinstance(input_anchor_configs, list):
            input_anchor_configs = [input_anchor_configs]

        return [
            InputAnchor(config["@Name"], config["@Optional"].lower() == "True")
            for config in input_anchor_configs
        ]

    def build_output_anchors(self):
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        output_anchor_configs = anchor_settings["OutputConnections"]["Connection"]
        if not isinstance(output_anchor_configs, list):
            output_anchor_configs = [output_anchor_configs]

            return [
                OutputAnchor(config["@Name"], config["@Optional"].lower() == "True", self._output_anchor_mgr)
                for config in output_anchor_configs
            ]
