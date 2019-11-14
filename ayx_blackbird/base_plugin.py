from typing import List, Optional

from .callback_strategy import UpdateOnlyCallbackStrategy, WorkflowRunCallbackStrategy
from .connection_interface import ConnectionInterface, ConnectionStatus
from .engine_proxy import EngineProxy
from .events import ConnectionEvents, PluginEvents
from .input_anchor import InputAnchor
from .observable_mixin import ObservableMixin
from .tool_config import ToolConfiguration
from .workflow_config import WorkflowConfiguration


class BasePlugin(ObservableMixin):
    def __init__(self, tool_id: int, alteryx_engine, output_anchor_mgr):
        ObservableMixin.__init__(self)

        self.engine = EngineProxy(alteryx_engine, tool_id)

        self.tool_config = ToolConfiguration(self.tool_name, output_anchor_mgr)

        self.input_anchors = self.tool_config.build_input_anchors()
        self.output_anchors = self.tool_config.build_output_anchors()

        # These properties get assigned in pi_init
        self.workflow_config = None

    def pi_init(self, workflow_config_xml_string: str) -> None:
        self.workflow_config = WorkflowConfiguration(workflow_config_xml_string)

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
            success = self.initialize_plugin()
            if success:
                self.on_complete()
                self.close_output_anchors()

            return success

        self.engine.error(self.engine.xmsg("Missing Incoming Connection(s)."))
        return False

    def pi_close(self, b_has_errors: bool) -> None:
        """pi_close is useless. Never use it."""
        pass

    def push_all_records(self) -> None:
        for anchor in self.output_anchors:
            anchor.push_records()

    def push_all_metadata(self) -> None:
        if not self._metadata_pushed:
            for anchor in self.output_anchors:
                anchor.push_metadata()

    def close_output_anchors(self) -> None:
        for anchor in self.output_anchors:
            anchor.close()

    def clear_all_input_records(self) -> None:
        for anchor in self.input_anchors:
            for connection in anchor.connections:
                connection.record_container.clear_records()

    def _run_plugin_initialization(self):
        self.notify_topic(PluginEvents.PLUGIN_INITIALIZED, self.initialize_plugin())

    def _build_connection(self, name: str) -> ConnectionInterface:
        connection_interface = ConnectionInterface(self, name)
        connection_interface.subscribe(
            ConnectionEvents.CONNECTION_INITIALIZED,
            self.callback_strategy.connection_initialized_callback,
        )
        connection_interface.subscribe(
            ConnectionEvents.RECORD_RECEIVED,
            self.callback_strategy.single_record_received_callback,
        )
        connection_interface.subscribe(
            ConnectionEvents.CONNECTION_CLOSED,
            self.callback_strategy.connection_closed_callback,
        )
        connection_interface.subscribe(
            ConnectionEvents.PROGRESS_UPDATE,
            self.callback_strategy.update_progress_callback,
        )

        return connection_interface

    @property
    def callback_strategy(self):
        return (
            WorkflowRunCallbackStrategy
            if not self.engine.update_only_mode
            else UpdateOnlyCallbackStrategy
        )

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

    """All properties below this point can/should be overridden for custom tools."""
    @property
    def tool_name(self) -> str:
        return "BlackbirdExample"

    @property
    def record_batch_size(self) -> Optional[int]:
        return 1

    def initialize_plugin(self) -> bool:
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.output_anchors[0].record_info = (
            self.input_anchors[0].connections[0].record_info
        )
        self.push_all_metadata()
        self.engine.info(self.engine.xmsg("Metadata built."))
        return True

    def process_records(self) -> None:
        self.output_anchors[0].record_container = (
            self.input_anchors[0].connections[0].record_container.copy()
        )
        self.push_all_records()

    def on_complete(self) -> None:
        self.engine.info(self.engine.xmsg("Completed processing records."))
