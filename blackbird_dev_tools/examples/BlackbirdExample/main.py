"""Example tool."""
from ayx_blackbird import BasePlugin
from ayx_blackbird.records import RawRecordContainer, RecordAccumulator


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdExample"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return None

    def set_record_accumulators(self):
        """Set the accumulator class for each connection."""
        for anchor in self.input_anchors:
            for connection in anchor.connections:
                connection.record_accumulator = RecordAccumulator(
                    raw_record_container=RawRecordContainer(connection.record_info)
                )

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor = self.get_output_anchor("Output")

        output_record_info = self.input_anchor.connections[0].record_info.clone()

        self.output_anchor.record_info = output_record_info
        self.push_all_metadata()
        return True

    def process_records(self) -> None:
        """Process records in batches."""
        input_records = self.input_anchor.connections[
            0
        ].record_accumulator.raw_record_container.records
        self.output_anchor.push_records(input_records)

        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
