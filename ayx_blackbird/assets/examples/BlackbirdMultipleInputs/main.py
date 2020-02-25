"""Example tool."""
import AlteryxPythonSDK as Sdk

from ayx_blackbird.core import BasePlugin, ConnectionInterface
from ayx_blackbird.records import generate_records_from_df
from ayx_blackbird.utilities.exceptions import WorkflowRuntimeError


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    def __init__(
        self,
        tool_id: int,
        alteryx_engine: Sdk.AlteryxEngine,
        output_anchor_mgr: Sdk.OutputAnchorManager,
    ):
        """Construct a plugin."""
        super().__init__(tool_id, alteryx_engine, output_anchor_mgr)
        self.output_anchor = None

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdMultipleInputs"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 1000

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.output_anchor = self.get_output_anchor("Output")
        self.engine.info(self.engine.xmsg("Plugin initialized."))

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)
        if self.output_anchor.record_info is None:
            self.output_anchor.record_info = connection.record_info
            self.push_all_metadata()

        incoming_names = [field.name for field in connection.record_info]
        incoming_types = [field.type for field in connection.record_info]

        outgoing_names = [field.name for field in self.output_anchor.record_info]
        outgoing_types = [field.type for field in self.output_anchor.record_info]

        if incoming_names != outgoing_names or incoming_types != outgoing_types:
            raise WorkflowRuntimeError(
                "Incoming metadata must be the same for all anchors."
            )

    def on_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        input_df = connection.record_containers[0].build_dataframe()

        self.output_anchor.push_records(
            generate_records_from_df(input_df, self.output_anchor.record_info)
        )

        connection.clear_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
