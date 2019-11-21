from ayx_blackbird import BasePlugin


class AyxPlugin(BasePlugin):
    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdExample"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 1000

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor = self.get_output_anchor("Output")

        self.output_anchor.record_info = self.input_anchor.connections[
            0
        ].record_info.clone()
        self.push_all_metadata()
        return True

    def process_records(self) -> None:
        """Process records in batches."""
        self.output_anchor.record_container.set_records(
            self.input_anchor.connections[0].record_container
        )

        self.push_all_records()
        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalizer for plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
