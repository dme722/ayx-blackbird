"""Example tool."""
from ayx_blackbird.core import BasePlugin, ConnectionInterface


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdOutput"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""

    def process_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        # Do nothing with records for now, this is an output tool
        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
