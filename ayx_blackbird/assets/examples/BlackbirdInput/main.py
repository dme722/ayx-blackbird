"""Example tool."""
from typing import Any

import AlteryxPythonSDK as Sdk

from ayx_blackbird.core import BasePlugin
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
        return "BlackbirdInput"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return None

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.output_anchor = self.get_output_anchor("Output")

        output_record_info = self.engine.create_record_info()
        output_record_info.add_field("x", Sdk.FieldType.float)
        output_record_info.add_field("y", Sdk.FieldType.v_wstring, size=100)
        output_record_info.add_field("z", Sdk.FieldType.float)

        self.output_anchor.record_info = output_record_info
        self.push_all_metadata()
        self.engine.info(self.engine.xmsg("Plugin initialized."))

    def on_incoming_records(self, *_: Any) -> None:
        """Do nothing. Input tools don't process records (they create them)."""
        pass

    def on_complete(self) -> None:
        """Create all records."""
        import pandas as pd

        workflow_config_value = self.workflow_config["Value"]
        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": ["hello", "world", "from blackbird"],
                "z": [
                    workflow_config_value,
                    workflow_config_value,
                    workflow_config_value,
                ],
            }
        )
        self.output_anchor.push_records(
            generate_records_from_df(df, self.output_anchor.record_info)
        )
        self.engine.info(self.engine.xmsg("Completed processing records."))
