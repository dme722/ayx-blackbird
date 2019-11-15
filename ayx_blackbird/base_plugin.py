from typing import List, Optional

from .anchor_utils_mixin import AnchorUtilsMixin
from .callback_strategy import ConnectionCallbackStrategy, UpdateOnlyConnectionCallbackStrategy, WorkflowRunConnectionCallbackStrategy
from .connection_interface import ConnectionInterface
from .engine_proxy import EngineProxy
from .events import ConnectionEvents, PluginEvents
from .input_anchor import InputAnchor
from .observable_mixin import ObservableMixin
from .tool_config import ToolConfiguration
from .workflow_config import WorkflowConfiguration


class BasePlugin(AnchorUtilsMixin, ObservableMixin):
    """Base plugin to inherit from."""
    def __init__(self, tool_id: int, alteryx_engine, output_anchor_mgr):
        AnchorUtilsMixin.__init__(self)
        ObservableMixin.__init__(self)

        self.engine = EngineProxy(alteryx_engine, tool_id)

        self.tool_config = ToolConfiguration(self.tool_name, output_anchor_mgr)

        self.input_anchors = self.tool_config.build_input_anchors()
        self.output_anchors = self.tool_config.build_output_anchors()

        # These properties get assigned in pi_init
        self.workflow_config = None

    def pi_init(self, workflow_config_xml_string: str) -> None:
        """Plugin initialization from the engine."""
        self.workflow_config = WorkflowConfiguration(workflow_config_xml_string)

    def pi_add_incoming_connection(
        self, anchor_name: str, connection_name: str
    ) -> ConnectionInterface:
        """Add incoming connection to the tool from the engine."""
        anchor = [a for a in self.input_anchors if a.name == anchor_name][0]

        connection = ConnectionInterface(self, connection_name)
        anchor.connections.append(connection)
        self._subscribe_to_connection(connection)
        return connection

    def _subscribe_to_connection(self, connection: ConnectionInterface):
        """Subscribe to events of interest generated by a connection."""
        connection.subscribe(
            ConnectionEvents.CONNECTION_INITIALIZED,
            self.callback_strategy.connection_initialized_callback,
        )
        connection.subscribe(
            ConnectionEvents.RECORD_RECEIVED,
            self.callback_strategy.single_record_received_callback,
        )
        connection.subscribe(
            ConnectionEvents.CONNECTION_CLOSED,
            self.callback_strategy.connection_closed_callback,
        )
        connection.subscribe(
            ConnectionEvents.PROGRESS_UPDATE,
            self.callback_strategy.update_progress_callback,
        )

    def pi_add_outgoing_connection(self, anchor_name: str) -> bool:
        """Register an outgoing connection from this tool."""
        anchor = [a for a in self.output_anchors if a.name == anchor_name][0]
        anchor.num_connections += 1
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        """Push all records when no inputs are connected."""
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

    def _run_plugin_initialization(self):
        """Run initialize plugin code."""
        self.notify_topic(PluginEvents.PLUGIN_INITIALIZED, self.initialize_plugin())

    @property
    def callback_strategy(self) -> ConnectionCallbackStrategy:
        """Generate the callback strategy for the tool"""
        return (
            UpdateOnlyConnectionCallbackStrategy
            if not self.engine.update_only_mode
            else WorkflowRunConnectionCallbackStrategy
        )

    @property
    def required_input_anchors(self) -> List[InputAnchor]:
        """Get the list of required input anchors for this tool."""
        return [anchor for anchor in self.input_anchors if not anchor.optional]

    """All properties below this point can/should be overridden for custom tools."""
    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdExample"

    @property
    def record_batch_size(self) -> Optional[int]:
        """Get the record batch size."""
        return 1

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.output_anchors[0].record_info = (
            self.input_anchors[0].connections[0].record_info
        )
        self.push_all_metadata()
        self.engine.info(self.engine.xmsg("Metadata built."))
        return True

    def process_records(self) -> None:
        """Process records in batches."""
        self.output_anchors[0].record_container = (
            self.input_anchors[0].connections[0].record_container.copy()
        )
        self.push_all_records()
        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalizer for plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
