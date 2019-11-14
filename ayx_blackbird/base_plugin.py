from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import List, Optional

from .connection_interface import ConnectionInterface, ConnectionStatus
from .engine_mixin import EngineMixin
from .events import ConnectionEvents, PluginEvents
from .input_anchor import InputAnchor
from .observable_mixin import ObservableMixin
from .tool_config import ToolConfiguration
from .workflow_config import WorkflowConfiguration


class BasePlugin(ABC, EngineMixin, ObservableMixin):
    @property
    @abstractmethod
    def tool_name(self) -> str:
        pass

    @property
    @abstractmethod
    def record_batch_size(self) -> Optional[int]:
        pass

    @abstractmethod
    def initialize_plugin(self) -> bool:
        pass

    @abstractmethod
    def build_metadata(self) -> None:
        pass

    @abstractmethod
    def process_records(self) -> None:
        pass

    @abstractmethod
    def on_complete(self) -> None:
        pass

    def __init__(self, n_tool_id: int, alteryx_engine, output_anchor_mgr):
        self.workflow_config = None
        self.user_data = SimpleNamespace()
        self.initialized = False
        self.tool_id = n_tool_id
        self.engine = alteryx_engine
        self.output_anchor_mgr = output_anchor_mgr
        self.tool_config = ToolConfiguration(self.tool_name, self.output_anchor_mgr)
        self.input_anchors = self.tool_config.build_input_anchors()
        self.output_anchors = self.tool_config.build_output_anchors()

        self._metadata_built = False

        ObservableMixin.__init__(self)

    def pi_init(self, workflow_config_xml_string: str) -> None:
        self.workflow_config = WorkflowConfiguration(
            workflow_config_xml_string, self.engine
        )

        if self.update_only_mode and len(self.required_input_anchors) == 0:
            self.initialized = self.initialize_plugin()

    def pi_add_incoming_connection(
        self, anchor_name: str, connection_name: str
    ) -> ConnectionInterface:
        anchor = [a for a in self.input_anchors if a.name == anchor_name][0]
        anchor.connections.append(self._build_connection(connection_name))
        return anchor.connections[-1]

    def pi_add_outgoing_connection(self, anchor_name: str) -> bool:
        anchor = [a for a in self.output_anchors if a.name == anchor_name][0]
        anchor.num_connections += 1
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        if len(self.required_input_anchors) == 0:
            self.build_metadata_if_not_already_build()
            self.on_complete()
            self.push_all_metadata()
            self.push_all_records()
            self.close_output_anchors()
        else:
            self.error(self.xmsg("Missing Incoming Connection(s)."))
            return False

        return True

    def pi_close(self, b_has_errors: bool) -> None:
        # pi_close is useless. Never use it.
        pass

    def push_all_records(self) -> None:
        for anchor in self.output_anchors:
            anchor.push_records()

    def push_all_metadata(self) -> None:
        for anchor in self.output_anchors:
            anchor.push_metadata()

    def close_output_anchors(self) -> None:
        for anchor in self.output_anchors:
            anchor.close()

    def clear_all_input_records(self) -> None:
        for anchor in self.input_anchors:
            for connection in anchor.connections:
                connection.record_container.clear_records()

    def update_progress(self, _: ConnectionInterface) -> None:
        import numpy as np

        percent = np.mean(
            [
                connection.progress_percentage
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

        self.engine.output_tool_progress(self.tool_id, percent)

        for anchor in self.output_anchors:
            anchor.update_progress(percent)

    def connection_initialized_callback(self, _: ConnectionInterface) -> bool:
        if self.all_connections_initialized:
            success = self.initialize_plugin()

            if success:
                if self.update_only_mode:
                    self.build_metadata_if_not_already_build()
                    self.push_all_metadata()

            return success

        return True

    def single_record_received_callback(self, connection: ConnectionInterface) -> None:
        if len(connection.record_container) >= self.record_batch_size:
            self.build_metadata_if_not_already_build()

            if not self.update_only_mode:
                self.process_records()

            self.push_all_metadata()

            if not self.update_only_mode:
                self.push_all_records()
                self.clear_all_input_records()
            return

    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        if self.all_connections_closed:
            self.build_metadata_if_not_already_build()

            if not self.update_only_mode:
                self.process_records()
                self.on_complete()

            self.push_all_metadata()

            if not self.update_only_mode:
                self.push_all_records()
                self.clear_all_input_records()

            self.close_output_anchors()

    def build_metadata_if_not_already_build(self):
        if not self._metadata_built:
            self.build_metadata()
            self._metadata_built = True

    def _run_plugin_initialization(self):
        self.notify_topic(PluginEvents.PLUGIN_INITIALIZED, self.initialize_plugin())
        self.initialize_plugin()

    def _build_connection(self, name: str) -> ConnectionInterface:
        connection_interface = ConnectionInterface(self, name)
        connection_interface.subscribe(
            ConnectionEvents.CONNECTION_INITIALIZED,
            self.connection_initialized_callback,
        )
        connection_interface.subscribe(
            ConnectionEvents.RECORD_RECEIVED, self.single_record_received_callback
        )
        connection_interface.subscribe(
            ConnectionEvents.CONNECTION_CLOSED, self.connection_closed_callback
        )
        connection_interface.subscribe(
            ConnectionEvents.PROGRESS_UPDATE, self.update_progress
        )

        return connection_interface

    @property
    def all_connections_initialized(self) -> bool:
        return all(
            [
                connection.status != ConnectionStatus.CREATED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

    @property
    def all_connections_closed(self) -> bool:
        return all(
            [
                connection.status == ConnectionStatus.CLOSED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

    @property
    def required_input_anchors(self) -> List[InputAnchor]:
        return [anchor for anchor in self.input_anchors if not anchor.optional]
