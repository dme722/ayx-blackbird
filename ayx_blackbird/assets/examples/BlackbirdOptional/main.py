"""Example tool."""
import AlteryxPythonSDK as Sdk

from ayx_blackbird.core import BasePlugin
from ayx_blackbird.records import generate_records_from_df


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdOptional"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.input_anchor = self.get_input_anchor("Input")
        self.output_anchor = self.get_output_anchor("Output")

        if not self.input_anchor.connections:
            output_record_info = self.engine.create_record_info()
        else:
            output_record_info = self.input_anchor.connections[0].record_info.clone()

        output_record_info.add_field("x", Sdk.FieldType.float)

        self.output_anchor.record_info = output_record_info
        self.push_all_metadata()
        return True

    def process_records(self) -> None:
        """Process records in batches."""
        if self.input_anchor.connections:
            df = self.input_anchor.connections[0].record_containers[0].build_dataframe()
            df["x"] = self.workflow_config["Value"]
        else:
            import pandas as pd

            df = pd.DataFrame({"x": [self.workflow_config["Value"]]})

        self.output_anchor.push_records(
            generate_records_from_df(df, self.output_anchor.record_info)
        )

        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))
