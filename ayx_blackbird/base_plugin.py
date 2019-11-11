import os
import sys
from abc import ABC, abstractmethod 
from types import SimpleNamespace

from .input_anchor import InputAnchor
from .output_anchor import OutputAnchor
from .connection_interface import ConnectionInterface, ConnectionStatus

import AlteryxPythonSDK as sdk

import xmltodict

class BasePlugin(ABC):
    @abstractmethod
    def initialize_plugin(self):
        pass

    @abstractmethod
    def build_metadata(self):
        pass

    @abstractmethod
    def process_records(self):
        pass

    @abstractmethod
    def on_complete(self):
        pass

    @abstractmethod
    @property
    def tool_name(self):
        pass

    @property
    def update_only_mode(self):
        return (
            self.engine.get_init_var(
                self.tool_id, "UpdateOnly"
            )
            == "True"
        )

    @abstractmethod
    @property
    def _connection_interface_class(self):
        pass

    @abstractmethod
    @property
    def record_batch_size(self):
        pass

    @property
    def _required_input_anchors(self):
        return [anchor for anchor in self._input_anchors if not anchor.optional]

    @property
    def all_connections_initialized(self):
        return all(
            [
                connection.status != ConnectionStatus.CREATED 
                for anchor in self._input_anchors 
                for connection in anchor.connections
            ]
        )

    @property
    def all_connections_closed(self):
        return all(
            [
                connection.status == ConnectionStatus.CLOSED 
                for anchor in self._input_anchors 
                for connection in anchor.connections
            ]
        )

    def __init__(
        self,
        n_tool_id: int,
        alteryxengine: sdk.AlteryxEngine,
        output_anchor_mgr: sdk.OutputAnchorManager,
    ) -> None:
        self.workflow_config = {}
        self.user_data = SimpleNamespace()
        self._input_anchors = []
        self._output_anchors = []
        self.initialized = False
        self.tool_id = n_tool_id
        self.engine = alteryxengine
        self._output_anchor_mgr = output_anchor_mgr
        self._tool_config = self._get_tool_config()

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

    def xmsg(self, message):
        return message

    def error(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.error, message)
    
    def warning(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.warning, message)

    def info(self, message):
        self.engine.output_message(self.tool_id, sdk.EngineMessageType.info, message)

    def _get_tool_path(self):
        return os.path.join(self._get_tools_location(), self.tool_name)

    def _get_tools_location(self):
        admin_path = os.path.join(os.environ["APPDATA"], "Alteryx", "Tools")
        user_path = os.path.join(os.environ["PROGRAMDATA"], "Alteryx", "Tools")
        if os.path.abspath(admin_path) in __file__:
            return admin_path

        if os.path.abspath(user_path) in __file__:
            return user_path

        raise RuntimeError("Tool is not located in Alteryx install locations.")

    def pi_init(self, workflow_config_xml_string: str):
        self._update_sys_path()

        self._build_input_anchors()
        self._build_output_anchors()

        self.workflow_config = xmltodict.parse(workflow_config_xml_string)["Configuration"]

        if (
            self.update_only_mode
            and len(self._required_input_anchors) == 0
        ):
            self.initialized = self.initialize_plugin()

    def _update_sys_path(self):
        """Update the sys path to include the current tools libs."""
        tool_path = self._get_tool_path()
        sys.path.append(tool_path)
        sys.path.append(os.path.join(tool_path, "Lib", "site-packages"))

    def _build_input_anchors(self):
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        input_anchor_configs = anchor_settings["InputConnections"]["Connection"]
        if not isinstance(input_anchor_configs, list):
            input_anchor_configs = [input_anchor_configs]

        for config in input_anchor_configs:
            anchor_name = config["@Name"]
            anchor_optional = config["@Optional"].lower() == "True"

            self._input_anchors.append(InputAnchor(anchor_name, anchor_optional))

    def _build_output_anchors(self):
        anchor_settings = self._tool_config["AlteryxJavaScriptPlugin"]["GuiSettings"]

        output_anchor_configs = anchor_settings["OutputConnections"]["Connection"]
        if not isinstance(output_anchor_configs, list):
            output_anchor_configs = [output_anchor_configs]

        for config in output_anchor_configs:
            anchor_name = config["@Name"]
            anchor_optional = config["@Optional"].lower() == "True"

            engine_output_anchor = self._output_anchor_mgr.get_output_anchor(
                anchor_name
            )

            self._output_anchors.append(OutputAnchor(anchor_name, anchor_optional, engine_output_anchor))

    def pi_add_incoming_connection(self, anchor_name, connection_name):
        anchor = [a for a in self._input_anchors if a.name == anchor_name][0]
        connection_interface = self._connection_interface_class(self, anchor, connection_name)
        anchor.connections.append(connection_interface)

        return connection_interface

    def pi_add_outgoing_connection(self, anchor_name):
        anchor = [a for a in self._output_anchors if a.name == anchor_name][0]
        anchor.num_connections += 1

    def pi_push_all_records(self, n_record_limit):
        if len(self._required_input_anchors) == 0:
            self.build_metadata()

            if not self.update_only_mode:
                self.on_complete()

            self.push_metadata()
            self.push_all_records()
            self.close_output_anchors()
        else:
            self.error(self.xmsg("Missing Incoming Connection(s)."))
            return False

        return True

    def push_all_records(self):
        for anchor in self._output_anchors:
            anchor.push_records()

    def pi_close(self, b_has_errors):
        # pi_close is useless. Never use it. 
        pass

    def push_metadata(self):
        for anchor in self._output_anchors:
            anchor.push_metadata()

    def close_output_anchors(self):
        for anchor in self._output_anchors:
            anchor.close()

    def notify_single_record_received(self):
        for anchor in self._input_anchors:
            for connection in anchor.connections:
                if len(connection.record_list) >= self.record_batch_size:
                    self.build_metadata()
                    self.process_records()
                    self.push_metadata()
                    self.push_all_records()
                    return

    def update_progress(self):
        import numpy as np
        percent = np.mean(
            [
                connection.progress_percentage 
                for anchor in self._input_anchors 
                for connection in anchor.connections
            ]
        )

        self.engine.output_tool_progress(self.tool_id, percent)

        for anchor in self._output_anchors:
            anchor.update_progress(percent)

    def notify_connection_closed(self):
        if self.all_connections_closed:
            self.build_metadata()

            if self.update_only_mode:
                self.process_records()
                self.on_complete()

            self.push_metadata()

            if self.update_only_mode:
                self.push_all_records()
                
            self.close_output_anchors()

    def notify_connection_initialized(self):
        if self.all_connections_initialized:
            success = self.initialize_plugin()

            if success:            
                if self.update_only_mode:
                    self.build_metadata()
                    self.push_metadata()

            return success

        return True