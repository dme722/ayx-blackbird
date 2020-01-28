"""Example tool."""
from ayx_blackbird.core import BasePlugin
from ayx_blackbird.records import generate_records_from_df

import AlteryxPythonSDK as Sdk


class AyxPlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdPassthrough"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> bool:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.output_anchor = self.get_output_anchor("Output")

        output_record_info = self.engine.create_record_info()
        output_record_info.add_field("x", Sdk.FieldType.float)
        output_record_info.add_field("y", Sdk.FieldType.v_wstring)

        self.output_anchor.record_info = output_record_info
        self.push_all_metadata()
        return True

    def process_records(self) -> None:
        """Do nothing. Input tools don't process records (they create them)."""
        pass

    def on_complete(self) -> None:
        """Create all records."""
        import pandas as pd

        df = pd.DataFrame({"x": [1, 2, 3], "y": "hello", "world", "from blackbird"})
        self.output_anchor.push_records(generate_records_from_df(df))
        self.engine.info(self.engine.xmsg("Completed processing records."))
