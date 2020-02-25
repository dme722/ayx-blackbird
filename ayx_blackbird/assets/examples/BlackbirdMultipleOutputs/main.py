"""Example tool."""
import AlteryxPythonSDK as Sdk

from ayx_blackbird.core import BasePlugin, ConnectionInterface
from ayx_blackbird.records import generate_records_from_df


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
        self.input_anchor = None
        self.output_anchor1 = None
        self.output_anchor2 = None

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdMultipleOutputs"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor1 = self.get_output_anchor("Output1")
        self.output_anchor2 = self.get_output_anchor("Output2")

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)
        output_record_info = self.input_anchor.connections[0].record_info.clone()

        self.output_anchor1.record_info = output_record_info
        self.output_anchor2.record_info = output_record_info
        self.push_all_metadata()

    def on_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        input_df = connection.record_containers[0].build_dataframe()
        self.output_anchor1.push_records(
            generate_records_from_df(input_df, self.output_anchor1.record_info)
        )
        self.output_anchor2.push_records(
            generate_records_from_df(input_df, self.output_anchor1.record_info)
        )

        connection.clear_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
