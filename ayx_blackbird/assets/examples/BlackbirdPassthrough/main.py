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
        self.output_anchor = None

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdPassthrough"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.output_anchor = self.get_output_anchor("Output")

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)
        self.output_anchor.record_info = connection.record_info.clone()
        self.push_all_metadata()

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
