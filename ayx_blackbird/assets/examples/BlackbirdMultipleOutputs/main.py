"""Example tool."""
from ayx_blackbird.core import BasePlugin, ConnectionInterface
from ayx_blackbird.records import generate_records_from_df


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

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
        output_record_info = self.input_anchor.connections[0].record_info.clone()

        self.output_anchor1.record_info = output_record_info
        self.output_anchor2.record_info = output_record_info
        self.push_all_metadata()

    def process_incoming_records(self) -> None:
        """Process records in batches."""
        input_df = (
            self.input_anchor.connections[0].record_containers[0].build_dataframe()
        )
        self.output_anchor1.push_records(
            generate_records_from_df(input_df, self.output_anchor1.record_info)
        )
        self.output_anchor2.push_records(
            generate_records_from_df(input_df, self.output_anchor1.record_info)
        )

        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
