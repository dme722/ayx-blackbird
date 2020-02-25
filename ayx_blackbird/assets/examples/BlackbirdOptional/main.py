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
        self.output_anchor = None
        self.output_anchor_metadata = None

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdOptional"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor = self.get_output_anchor("Output")
        self.output_anchor_metadata = None

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)
        output_record_info = self.input_anchor.connections[0].record_info.clone()
        self.output_anchor_metadata = output_record_info

    def generate_metadata(self) -> None:
        """Build and push outgoing metadata."""
        if self.output_anchor_metadata is None:
            output_record_info = self.engine.create_record_info()
        else:
            output_record_info = self.output_anchor_metadata

        if self.output_anchor.record_info is None:
            output_record_info.add_field("optional_value", Sdk.FieldType.float)
            self.output_anchor_metadata = output_record_info

            self.output_anchor.record_info = self.output_anchor_metadata
            self.push_all_metadata()

    def on_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        self.generate_metadata()

        df = connection.record_containers[0].build_dataframe()
        df["optional_value"] = self.workflow_config["Value"]

        self.output_anchor.push_records(
            generate_records_from_df(df, self.output_anchor.record_info)
        )

        connection.clear_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        if not self.input_anchor.connections:
            self.generate_metadata()

            import pandas as pd

            df = pd.DataFrame({"optional_value": [self.workflow_config["Value"]]})
            self.output_anchor.push_records(
                generate_records_from_df(df, self.output_anchor.record_info)
            )

        self.engine.info(self.engine.xmsg("Completed processing records."))
