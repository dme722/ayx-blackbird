from abc import ABC, abstractmethod
from types import SimpleNamespace

from .connection_interface import ConnectionInterface, ConnectionStatus
from .engine_mixin import EngineMixin
from .tool_config import ToolConfiguration
from .workflow_config import WorkflowConfig


class BasePlugin(ABC, EngineMixin):
    @abstractmethod
    @property
    def tool_name(self):
        pass

    @abstractmethod
    @property
    def record_batch_size(self):
        pass

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

    def __init__(self, n_tool_id, alteryx_engine, output_anchor_mgr):
        self.workflow_config = None
        self.user_data = SimpleNamespace()
        self.input_anchors = None
        self.output_anchors = None
        self.initialized = False
        self.tool_id = n_tool_id
        self.engine = alteryx_engine
        self.output_anchor_mgr = output_anchor_mgr
        self.tool_config = ToolConfiguration(self.tool_name)

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

    @property
    def required_input_anchors(self):
        return [anchor for anchor in self._input_anchors if not anchor.optional]

    def pi_init(self, workflow_config_xml_string: str):
        self._input_anchors = self._tool_config.build_input_anchors()
        self._output_anchors = self._tool_config.build_output_anchors()

        self.workflow_config = WorkflowConfig(workflow_config_xml_string, self.engine)

        if (
            self.update_only_mode
            and len(self._required_input_anchors) == 0
        ):
            self.initialized = self.initialize_plugin()

    def pi_add_incoming_connection(self, anchor_name, connection_name):
        anchor = [a for a in self._input_anchors if a.name == anchor_name][0]
        connection_interface = ConnectionInterface(self, anchor, connection_name)
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

    def single_record_received_callback(self):
        for anchor in self._input_anchors:
            for connection in anchor.connections:
                if len(connection.record_list) >= self.record_batch_size:
                    self.build_metadata()

                    if not self.update_only_mode:
                        self.process_records()

                    self.push_metadata()

                    if not self.update_only_mode:
                        self.push_all_records()
                    return
    
    def connection_closed_callback(self):
        if self.all_connections_closed:
            self.build_metadata()

            if self.update_only_mode:
                self.process_records()
                self.on_complete()

            self.push_metadata()

            if self.update_only_mode:
                self.push_all_records()

            self.close_output_anchors()

    def connection_initialized_callback(self):
        if self.all_connections_initialized:
            success = self.initialize_plugin()

            if success:
                if self.update_only_mode:
                    self.build_metadata()
                    self.push_metadata()

            return success

        return True
