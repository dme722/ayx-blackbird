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

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)

    def on_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        # Do nothing with records for now, this is an output tool
        connection.clear_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
