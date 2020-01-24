import AlteryxPythonSDK as sdk

from ayx_blackbird import BasePlugin
from ayx_blackbird.records import generate_records_from_df


class AyxPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # import cProfile
        # self.pr = cProfile.Profile()
        # self.pr.enable()

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "TestTool"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return None

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
        # import pandas as pd

        input_df = self.input_anchor.connections[0].record_accumulator.parsed_record_container.dataframe
        self.output_anchor.push_records(generate_records_from_df(input_df, self.output_anchor.record_info))

        self.clear_all_input_records()

    def on_complete(self) -> None:
        """Finalizer for plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))

        # import pstats
        # self.pr.disable()
        # ps = pstats.Stats(self.pr).sort_stats('cumulative')
        # ps.dump_stats('C:\\Users\\dellison\\Desktop\\profile.pstats')
